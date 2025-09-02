"""
Smithery FastMCP Patch - Session Config Support

This provides a wrapper for FastMCP that adds session-scoped configuration support,
"""

import base64
import json
import inspect
from typing import Any, Dict, Optional, Type, get_type_hints

from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, ValidationError
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware


# Global session config storage
_session_configs: Dict[str, Dict[str, Any]] = {}


class _FastMCPWrapper:
    """Internal wrapper that adds session config support to FastMCP."""
    
    def __init__(self, fastmcp_instance: FastMCP, config_schema: Optional[Type[BaseModel]] = None):
        self._fastmcp = fastmcp_instance
        self._config_schema = config_schema
        
        # Patch the instance methods
        self._patch_streamable_http_app()
        self._patch_decorators()
        
        # Forward all FastMCP attributes and methods
        self._forward_attributes()
    
    def _forward_attributes(self):
        """Forward essential FastMCP attributes and methods to this wrapper."""
        # Forward essential methods that are commonly used
        essential_methods = ['get_context', 'run']
        
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
            
            # Add session config middleware
            app.add_middleware(SessionConfigMiddleware, config_schema=self._config_schema)
            return app
        
        # Replace the method on the wrapper
        self.streamable_http_app = patched_streamable_http_app
    
    def _patch_decorators(self):
        """Patch all decorators (tool, resource, prompt) to support config injection."""
        
        def create_config_aware_decorator(original_decorator_method):
            """Create a config-aware version of any decorator."""
            def patched_decorator(*args, **kwargs):
                original_decorator = original_decorator_method(*args, **kwargs)
                
                def config_aware_decorator(fn):
                    # Check if function wants config injection
                    sig = inspect.signature(fn)
                    type_hints = get_type_hints(fn)
                    
                    config_param = None
                    for param_name in sig.parameters:
                        if param_name == 'config' or (param_name in type_hints and 
                            self._config_schema and 
                            issubclass(type_hints[param_name], self._config_schema)):
                            config_param = param_name
                            break
                    
                    if config_param:
                        # Wrap function to inject config
                        async def wrapped_fn(*fn_args, **fn_kwargs):
                            # Get current session config
                            ctx = self._fastmcp.get_context()
                            session_config = getattr(ctx, 'session_config', {})
                            
                            # Convert to Pydantic model if schema provided
                            if self._config_schema:
                                try:
                                    config_obj = self._config_schema(**session_config)
                                except ValidationError:
                                    config_obj = self._config_schema()
                            else:
                                config_obj = session_config
                            
                            # Inject config
                            fn_kwargs[config_param] = config_obj
                            
                            if inspect.iscoroutinefunction(fn):
                                return await fn(*fn_args, **fn_kwargs)
                            else:
                                return fn(*fn_args, **fn_kwargs)
                        
                        return original_decorator(wrapped_fn)
                    else:
                        return original_decorator(fn)
                
                return config_aware_decorator
            return patched_decorator
        
        # Patch all decorator methods
        self.tool = create_config_aware_decorator(self._fastmcp.tool)
        self.resource = create_config_aware_decorator(self._fastmcp.resource)
        self.prompt = create_config_aware_decorator(self._fastmcp.prompt)


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
            # Only extract config from URL query params
            try:
                config = self._parse_and_validate_config_from_url(scope)
                
                # Check if this is an existing session by looking for session ID
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
                    # New session (initialize request) - store config for when session ID is created
                    temp_key = f"temp_{id(scope)}"
                    _session_configs[temp_key] = config
                    scope["temp_config_key"] = temp_key
                    scope["session_config"] = config
                
            except ValueError:
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
    
    def _parse_and_validate_config_from_url(self, scope) -> Dict[str, Any]:
        """Parse and validate config from URL query parameters only."""
        config = {}
        
        # Extract query string from scope
        query_string = scope.get("query_string", b"").decode("utf-8")
        if not query_string:
            return config
        
        # Parse query parameters manually
        from urllib.parse import parse_qsl
        query_params = dict(parse_qsl(query_string))
        
        # 1. Process base64-encoded config parameter
        config_param = query_params.get('config')
        if config_param:
            try:
                config_json = base64.b64decode(config_param).decode('utf-8')
                base_config = json.loads(config_json)
                config.update(base_config)
            except (ValueError, json.JSONDecodeError) as e:
                raise ValueError(f"Invalid config parameter: {e}")
        
        # 2. Process simple query parameters
        for key, value in query_params.items():
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


def from_fastmcp(
    fastmcp_instance: FastMCP, 
    *, 
    config_schema: Optional[Type[BaseModel]] = None
) -> FastMCP:
    """
    Patch a FastMCP instance with session-scoped configuration support and CORS.
    
    Automatically adds CORS middleware with permissive settings for development.
    
    Args:
        fastmcp_instance: The FastMCP instance to patch
        config_schema: Optional Pydantic model for config validation
        
    Returns:
        Patched FastMCP instance with session config support and CORS enabled
        
    Example:
        ```python
        from mcp.server.fastmcp import FastMCP
        from smithery.server.fastmcp_patch import from_fastmcp
        
        class MyConfig(BaseModel):
            api_key: str
            debug: bool = False
        
        app = from_fastmcp(FastMCP(), config_schema=MyConfig)
        
        @app.tool()
        def my_tool(query: str, config: MyConfig):
            # Config is automatically injected per session
            # CORS is automatically enabled for browser access
            if config.debug:
                print(f"Debug: Processing {query}")
            # Use config.api_key...
        ```
    """
    return _FastMCPWrapper(fastmcp_instance, config_schema)




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
        except (AttributeError, KeyError):
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
