"""
Patched FastMCP with native session-scoped configuration support.

This extends FastMCP to add session config management directly into the framework,
making it as elegant as the TypeScript implementation but with even better DX.
"""

import base64
import json
import inspect
from typing import Any, Dict, Optional, Type, get_type_hints
from contextlib import contextmanager

from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


# Global session config storage
_session_configs: Dict[str, Dict[str, Any]] = {}


class SessionConfigMixin:
    """Mixin to add session config support to FastMCP."""
    
    def __init__(self, *args, session_config_schema: Optional[Type[BaseModel]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._session_config_schema = session_config_schema
        
        # Patch the session manager to handle config extraction
        self._patch_session_manager()
    
    def _patch_session_manager(self):
        """Patch the StreamableHTTP session manager to extract config during initialize."""
        # Store original method
        original_method = self.streamable_http_app
        
        def patched_streamable_http_app():
            app = original_method()
            
            # Add middleware to extract config during initialize
            from starlette.middleware import Middleware
            app.add_middleware(SessionConfigMiddleware, config_schema=self._session_config_schema)
            
            return app
        
        # Replace the method on this instance
        self.streamable_http_app = patched_streamable_http_app
    
    def _patch_tool_calling(self):
        """Patch tool calling to inject config parameters."""
        # This will be implemented to automatically inject config into tool functions
        pass


class SessionConfigMiddleware:
    """Middleware to extract and store session config during initialize."""
    
    def __init__(self, app, config_schema=None):
        self.app = app
        self.config_schema = config_schema
    
    async def __call__(self, scope, receive, send):
        # Only process HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # For MCP requests, extract config from URL and store in scope
        if scope["method"] == "POST" and scope["path"] == "/mcp":
            request = Request(scope, receive)
            
            # Always try to extract config from URL (never read body!)
            try:
                config = self._parse_and_validate_config(request)
                
                # Check if this is an initialize request by looking for session ID
                session_id = None
                for name, value in scope.get("headers", []):
                    if name == b"mcp-session-id":
                        session_id = value.decode()
                        break
                
                if session_id:
                    # Existing session - use stored config
                    if session_id in _session_configs:
                        scope["session_config"] = _session_configs[session_id]
                    else:
                        scope["session_config"] = {}
                else:
                    # New session (initialize) - store config for later
                    temp_key = f"temp_{id(request)}"
                    _session_configs[temp_key] = config
                    scope["temp_config_key"] = temp_key
                    scope["session_config"] = config
                
            except ValueError as e:
                # Config validation failed - let it through, FastMCP will handle the error
                scope["session_config"] = {}
        
        # Wrap send to capture session ID from response headers
        original_send = send
        
        async def wrapped_send(message):
            if message["type"] == "http.response.start":
                # Check for session ID in response headers
                temp_key = scope.get("temp_config_key")
                if temp_key:
                    for name, value in message.get("headers", []):
                        if name == b"mcp-session-id":
                            session_id = value.decode()
                            # Move config from temp key to actual session ID
                            if temp_key in _session_configs:
                                config = _session_configs.pop(temp_key)
                                _session_configs[session_id] = config
                            break
            
            await original_send(message)
        
        await self.app(scope, receive, wrapped_send)
    
    def _parse_and_validate_config(self, request: Request) -> Dict[str, Any]:
        """Parse and validate config from request."""
        config = {}
        
        # 1. Process base64-encoded config parameter
        config_param = request.query_params.get('config')
        if config_param:
            try:
                config_json = base64.b64decode(config_param).decode('utf-8')
                base_config = json.loads(config_json)
                config.update(base_config)
            except (ValueError, json.JSONDecodeError) as e:
                raise ValueError(f"Invalid config parameter: {e}")
        
        # 2. Process simple query parameters
        for key, value in request.query_params.items():
            if key in ('config',):
                continue
            
            # Try to parse as JSON
            try:
                parsed_value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                parsed_value = value
            
            config[key] = parsed_value
        
        # 3. Validate against schema
        if self.config_schema:
            try:
                validated_config = self.config_schema(**config)
                return validated_config.model_dump()
            except ValidationError as e:
                raise ValueError(f"Config validation failed: {e}")
        
        return config


class PatchedFastMCP(SessionConfigMixin, FastMCP):
    """FastMCP with native session config support."""
    
    def __init__(self, *args, session_config_schema: Optional[Type[BaseModel]] = None, **kwargs):
        super().__init__(*args, session_config_schema=session_config_schema, **kwargs)
    
    def tool(self, *args, **kwargs):
        """Enhanced tool decorator that supports config injection."""
        original_decorator = super().tool(*args, **kwargs)
        
        def enhanced_decorator(fn):
            # Check if function wants config injection
            sig = inspect.signature(fn)
            type_hints = get_type_hints(fn)
            
            # Look for config parameter
            config_param = None
            for param_name, param in sig.parameters.items():
                if param_name == 'config' or (param_name in type_hints and 
                    self._session_config_schema and 
                    issubclass(type_hints[param_name], self._session_config_schema)):
                    config_param = param_name
                    break
            
            if config_param:
                # Wrap the function to inject config
                async def wrapped_fn(*fn_args, **fn_kwargs):
                    # Get current session config
                    ctx = self.get_context()
                    session_config = getattr(ctx, 'session_config', {})
                    
                    # Convert to Pydantic model if schema is provided
                    if self._session_config_schema:
                        try:
                            config_obj = self._session_config_schema(**session_config)
                        except ValidationError:
                            config_obj = self._session_config_schema()
                    else:
                        config_obj = session_config
                    
                    # Inject config into function call
                    fn_kwargs[config_param] = config_obj
                    
                    if inspect.iscoroutinefunction(fn):
                        return await fn(*fn_args, **fn_kwargs)
                    else:
                        return fn(*fn_args, **fn_kwargs)
                
                # Apply original decorator to wrapped function
                return original_decorator(wrapped_fn)
            else:
                # No config injection needed
                return original_decorator(fn)
        
        return enhanced_decorator


# Patch the Context class to include session config
def patch_context_with_session_config():
    """Patch the FastMCP Context class to include session_config property."""
    
    @property
    def session_config(self) -> Dict[str, Any]:
        """Get the session configuration."""
        try:
            # Try to get from request scope
            if hasattr(self.request_context, 'request') and hasattr(self.request_context.request, 'scope'):
                return self.request_context.request.scope.get('session_config', {})
            
            # Fallback: get by session ID
            session_id = getattr(self.request_context.session, 'session_id', None)
            if session_id and session_id in _session_configs:
                return _session_configs[session_id]
        except:
            pass
        
        return {}
    
    # Add the property to Context class
    Context.session_config = session_config


# Apply the context patch
patch_context_with_session_config()


# Utility functions
def get_session_config(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get config for a session."""
    if session_id and session_id in _session_configs:
        return _session_configs[session_id]
    return {}


def cleanup_session_config(session_id: str):
    """Clean up session config."""
    _session_configs.pop(session_id, None)
