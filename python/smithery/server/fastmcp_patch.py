"""
Smithery FastMCP Patch - Session Config Support

This provides a wrapper for FastMCP that adds session-scoped configuration support.
"""

import json
from typing import Any, Dict, Optional, Type

from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, ValidationError
from starlette.middleware.cors import CORSMiddleware


class _FastMCPWrapper:
    """Internal wrapper that adds session config support to FastMCP."""
    
    def __init__(self, fastmcp_instance: FastMCP, config_schema: Optional[Type[BaseModel]] = None):
        self._fastmcp = fastmcp_instance
        self._config_schema = config_schema
        
        # Patch the instance methods
        self._patch_streamable_http_app()
        
        # Forward all FastMCP attributes and methods
        self._forward_attributes()
    
    def _forward_attributes(self):
        """Forward essential FastMCP attributes and methods to this wrapper."""
        # Forward essential methods that are commonly used
        essential_methods = ['get_context', 'run', 'tool', 'resource', 'prompt']
        
        for method_name in essential_methods:
            if hasattr(self._fastmcp, method_name):
                method = getattr(self._fastmcp, method_name)
                def make_forwarder(m):
                    def forwarder(*args, **kwargs):
                        return m(*args, **kwargs)
                    return forwarder
                setattr(self, method_name, make_forwarder(method))
        
        # Forward settings as a lazy property
        @property
        def settings(self):
            return self._fastmcp.settings
        
        self.__class__.settings = settings
    
    def _patch_streamable_http_app(self):
        """Patch the StreamableHTTP app to add CORS and session config middleware."""
        original_method = self._fastmcp.streamable_http_app
        
        def patched_streamable_http_app():
            app = original_method()
            
            # Add CORS middleware first (outer layer)
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["GET", "POST", "DELETE"],
                allow_headers=["Content-Type", "Accept", "mcp-session-id"],
                expose_headers=["mcp-session-id"]
            )
            
            # Add session config middleware to extract config from URL
            app.add_middleware(SessionConfigMiddleware, config_schema=self._config_schema)
            
            return app
        
        # Replace the method on the actual FastMCP instance
        self._fastmcp.streamable_http_app = patched_streamable_http_app
    



class SessionConfigMiddleware:
    """Middleware to extract config from URL parameters and store in request scope."""
    
    def __init__(self, app, config_schema=None):
        self.app = app
        self.config_schema = config_schema
    
    async def __call__(self, scope, receive, send):
        # Only process HTTP requests to MCP endpoint
        if scope["type"] != "http" or scope["method"] != "POST" or scope["path"] != "/mcp":
            await self.app(scope, receive, send)
            return
        
        # Parse config from URL parameters and store in scope
        try:
            raw_config = self._parse_config_from_url(scope)
            
            # Validate and create ConfigSchema instance
            if self.config_schema:
                try:
                    config_instance = self.config_schema(**raw_config)
                except ValidationError:
                    # Validation failed, use defaults
                    config_instance = self.config_schema()
            else:
                # No schema, store raw dict
                config_instance = raw_config
            
            # Store validated config instance in scope
            scope["session_config"] = config_instance
            
        except Exception:
            # Any error - use default config
            config_instance = self.config_schema() if self.config_schema else {}
            scope["session_config"] = config_instance
        
        await self.app(scope, receive, send)
    
    def _parse_config_from_url(self, scope) -> Dict[str, Any]:
        """Parse config from URL query parameters."""
        config = {}
        
        # Extract query string from scope
        query_string = scope.get("query_string", b"").decode("utf-8")
        if not query_string:
            return config
        
        # Parse query parameters
        from urllib.parse import parse_qsl
        query_params = dict(parse_qsl(query_string))
        
        # Convert query parameters to config dict
        for key, value in query_params.items():
            # Try to parse as JSON for proper typing
            try:
                parsed_value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                parsed_value = value
            
            config[key] = parsed_value
        
        return config


def from_fastmcp(
    fastmcp_instance: FastMCP, 
    *, 
    config_schema: Optional[Type[BaseModel]] = None
) -> FastMCP:
    """
    Add session config support and CORS to a FastMCP instance.
    
    Config is passed via URL parameters and accessed through ctx.session_config.
    
    Args:
        fastmcp_instance: FastMCP instance to enhance
        config_schema: Pydantic model for config validation
        
    Returns:
        Enhanced FastMCP instance
        
    Example:
        ```python
        class Config(BaseModel):
            debug: bool = False
        
        app = from_fastmcp(FastMCP(), config_schema=Config)
        
        @app.tool()
        def my_tool() -> str:
            config = app.get_context().session_config
            return f"Debug: {config.debug}"
        
        # Usage: POST /mcp?debug=true
        ```
    """
    return _FastMCPWrapper(fastmcp_instance, config_schema)




# Patch the Context class to include session config
def patch_context_with_session_config():
    """Patch the FastMCP Context class to include session_config property."""
    
    @property
    def session_config(self) -> Any:
        """Get the session configuration from request scope."""
        try:
            # Get config from request scope (set by middleware)
            if hasattr(self.request_context, 'request') and hasattr(self.request_context.request, 'scope'):
                scope = self.request_context.request.scope
                config = scope.get('session_config')
                
                if config is not None:
                    return config
            
        except (AttributeError, KeyError):
            pass
        
        return {}
    
    # Add the property to Context class
    Context.session_config = session_config


# Apply the context patch
patch_context_with_session_config()