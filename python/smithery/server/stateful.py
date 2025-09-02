"""
Stateful MCP Server implementation for Python.

This module provides a wrapper around FastMCP that adds per-request configuration support
using middleware to extract config from URL parameters.
"""

import base64
import json
import contextvars
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ValidationError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Global session config storage
_session_configs: Dict[str, Dict[str, Any]] = {}


class StatefulServerOptions(BaseModel):
    """Configuration options for the stateful server."""
    config_schema: Optional[Any] = None
    
    class Config:
        arbitrary_types_allowed = True


def parse_express_request_config(request: Request) -> Dict[str, Any]:
    """Parse base64-encoded config from request query parameters."""
    config_param = request.query_params.get('config')
    if not config_param:
        return {}
    
    try:
        config_json = base64.b64decode(config_param).decode('utf-8')
        return json.loads(config_json)
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse config parameter: {e}")


def parse_simple_query_config(query_params: Dict[str, str]) -> Dict[str, Any]:
    """Parse simple query parameters as config."""
    config = {}
    
    for key, value in query_params.items():
        # Skip reserved parameters
        if key in ('config',):
            continue
        
        # Try to parse value as JSON (for booleans, numbers, etc.)
        try:
            parsed_value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            # If parsing fails, use the raw string value
            parsed_value = value
        
        config[key] = parsed_value
    
    return config


def parse_and_validate_config(
    request: Request,
    config_schema: Optional[type] = None
) -> Dict[str, Any]:
    """Parse and validate config from request with optional Pydantic schema validation."""
    config = {}
    
    # 1. Process base64-encoded config parameter if present
    try:
        base_config = parse_express_request_config(request)
        config.update(base_config)
    except ValueError as e:
        raise ValueError(f"Invalid config parameter: {e}")
    
    # 2. Process simple query parameters
    query_dict = dict(request.query_params)
    query_config = parse_simple_query_config(query_dict)
    config.update(query_config)
    
    # 3. Validate against schema if provided
    if config_schema:
        try:
            validated_config = config_schema(**config)
            # Convert back to dict for storage
            return validated_config.model_dump()
        except ValidationError as e:
            raise ValueError(f"Config validation failed: {e}")
    
    return config


class SmitherySessionMiddleware(BaseHTTPMiddleware):
    """Middleware to handle session-scoped config and extract session ID."""
    
    def __init__(self, app, config_schema=None):
        super().__init__(app)
        self.config_schema = config_schema
    
    async def dispatch(self, request: Request, call_next):
        # Get session ID from header
        session_id = request.headers.get('mcp-session-id')
        
        # For initialize requests, extract and store config
        if request.url.path == "/mcp" and request.method == "POST":
            try:
                body = await request.json()
                method = body.get("method")
                
                # Handle initialize request - extract and store config by session
                if method == "initialize":
                    try:
                        config = parse_and_validate_config(request, self.config_schema)
                        # We'll get the actual session ID from FastMCP's response
                        # For now, store with a temporary key based on request
                        temp_key = f"temp_{id(request)}"
                        _session_configs[temp_key] = config
                        request.scope['temp_config_key'] = temp_key
                    except ValueError as e:
                        return JSONResponse(
                            status_code=400,
                            content={
                                "jsonrpc": "2.0",
                                "error": {
                                    "code": -32602,
                                    "message": str(e)
                                },
                                "id": body.get("id")
                            }
                        )
                
                # For other requests, get config from session storage
                elif session_id and session_id in _session_configs:
                    request.scope['smithery_config'] = _session_configs[session_id]
                else:
                    request.scope['smithery_config'] = {}
                    
            except Exception:
                # If we can't parse JSON, continue without config
                request.scope['smithery_config'] = {}
        else:
            request.scope['smithery_config'] = {}
        
        # Store session ID in scope for access by tools
        request.scope['session_id'] = session_id
        
        return await call_next(request)


class SessionIdMappingMiddleware(BaseHTTPMiddleware):
    """Middleware to map temporary config keys to actual session IDs after FastMCP processes initialize."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Check if this was an initialize request with a temp config key
        if hasattr(request.scope, 'temp_config_key'):
            temp_key = request.scope.get('temp_config_key')
            
            # Get the session ID from the response headers
            session_id = response.headers.get('mcp-session-id')
            
            if temp_key and session_id and temp_key in _session_configs:
                # Move config from temp key to actual session ID
                config = _session_configs.pop(temp_key)
                _session_configs[session_id] = config
        
        return response


def store_session_config(session_id: str, config: Dict[str, Any]):
    """Store config for a session."""
    _session_configs[session_id] = config


def get_session_config(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get config for a specific session or current session."""
    if session_id and session_id in _session_configs:
        return _session_configs[session_id]
    
    # Try to get from current request context
    try:
        ctx = contextvars.copy_context()
        for var, value in ctx.items():
            if hasattr(value, 'scope'):
                if 'smithery_config' in value.scope:
                    return value.scope['smithery_config']
                # Also check for session_id in scope to get config
                if 'session_id' in value.scope:
                    current_session_id = value.scope['session_id']
                    if current_session_id and current_session_id in _session_configs:
                        return _session_configs[current_session_id]
    except:
        pass
    
    return {}


def get_current_session_id() -> Optional[str]:
    """Get the current session ID from request context."""
    try:
        ctx = contextvars.copy_context()
        for var, value in ctx.items():
            if hasattr(value, 'scope') and 'session_id' in value.scope:
                return value.scope['session_id']
    except:
        pass
    return None


def cleanup_session(session_id: str):
    """Clean up session data."""
    _session_configs.pop(session_id, None)


# Backward compatibility functions
def get_request_config() -> Dict[str, Any]:
    """Get full config from current request context (backward compatibility)."""
    return get_session_config()


def get_config_value(key: str, default=None):
    """Get a specific config value from current session."""
    config = get_session_config()
    return config.get(key, default)


def create_stateful_server(
    mcp_server: FastMCP,
    options: Optional[StatefulServerOptions] = None
) -> Starlette:
    """
    Create a stateful server wrapper around FastMCP with per-request configuration.
    
    Args:
        mcp_server: FastMCP server instance
        options: Configuration options including optional schema validation
        
    Returns:
        Starlette application with config middleware
    """
    if options is None:
        options = StatefulServerOptions()
    
    # Add the config route directly to the FastMCP server using custom_route
    @mcp_server.custom_route("/.well-known/mcp-config", methods=["GET"])
    async def mcp_config_handler(request: Request) -> Response:
        """Handle GET requests for /.well-known/mcp-config endpoint."""
        base_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # If we have a Pydantic schema, convert it to JSON Schema
        if options.config_schema:
            try:
                # Create a dummy instance to get the schema
                schema_dict = options.config_schema.model_json_schema()
                base_schema = schema_dict
            except Exception:
                pass  # Fall back to empty schema
        
        config_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{request.url.scheme}://{request.headers.get('host', 'localhost')}/.well-known/mcp-config",
            "title": "MCP Session Configuration",
            "description": "Schema for the /mcp endpoint configuration",
            "x-mcp-version": "1.0",
            "x-query-style": "simple",
            **base_schema
        }
        
        return JSONResponse(
            content=config_schema,
            headers={"Content-Type": "application/schema+json; charset=utf-8"}
        )
    
    # Get FastMCP's app
    app = mcp_server.streamable_http_app()
    
    # Add our session-aware config middleware
    app.add_middleware(SmitherySessionMiddleware, config_schema=options.config_schema)
    
    # Add custom middleware to handle session ID mapping after FastMCP processes initialize
    app.add_middleware(SessionIdMappingMiddleware)
    
    # Add CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id", "mcp-protocol-version"],
        max_age=86400,
    )
    
    return app