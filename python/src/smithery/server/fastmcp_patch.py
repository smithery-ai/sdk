"""
Smithery FastMCP Patch - Session Config Support

This provides a wrapper for FastMCP that adds middleware for smithery session config and CORS.
"""

from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, ValidationError
from starlette.middleware.cors import CORSMiddleware

from ..utils.url import decode_config_from_base64


class SmitheryFastMCP:
    """Wrapper that adds session config and CORS to FastMCP."""

    def __init__(self, fastmcp_instance: FastMCP, config_schema: type[BaseModel] | None = None):
        self._fastmcp = fastmcp_instance
        self._config_schema = config_schema

        # Patch the instance methods
        self._patch_streamable_http_app()

    def __getattr__(self, name: str):
        """Forward all attribute access to the wrapped FastMCP instance."""
        # First check if the attribute exists on the wrapped instance
        if hasattr(self._fastmcp, name):
            attr = getattr(self._fastmcp, name)

            # If it's a callable (method), return it directly
            # Python will handle the binding automatically
            return attr

        # If attribute doesn't exist on wrapped instance, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _patch_streamable_http_app(self):
        """Patch the StreamableHTTP app to add CORS and session config middleware."""
        original_method = self._fastmcp.streamable_http_app

        def patched_streamable_http_app():
            app = original_method()

            # Add CORS middleware - minimal configuration for MCP compatibility
            # Key finding: mcp-protocol-version header is ESSENTIAL for tunnel/browser requests
            # OPTIONS method is handled automatically by Starlette CORS middleware
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["GET", "POST"],
                allow_headers=["Content-Type", "Accept", "mcp-session-id", "mcp-protocol-version"],
                expose_headers=["mcp-session-id", "mcp-protocol-version"],
                max_age=86400,
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

    def _parse_config_from_url(self, scope) -> dict[str, Any]:
        """Parse config from base64-encoded URL parameter."""
        # Extract query string from scope
        query_string = scope.get("query_string", b"").decode("utf-8")
        if not query_string:
            return {}

        # Parse query parameters
        from urllib.parse import parse_qsl
        query_params = dict(parse_qsl(query_string))

        # Look for base64-encoded config parameter
        if "config" in query_params:
            return decode_config_from_base64(query_params["config"])

        return {}


def from_fastmcp(
    fastmcp_instance: FastMCP,
    *,
    config_schema: type[BaseModel] | None = None
) -> SmitheryFastMCP:
    """
    Add session config support and CORS to a FastMCP instance.

    Config is passed via base64-encoded URL parameter (standard Smithery format)
    and accessed through ctx.session_config.

    Args:
        fastmcp_instance: FastMCP instance to patch
        config_schema: Optional Pydantic model for config validation and schema generation.

    Returns:
        Enhanced FastMCP instance

    Example:
        ```python
        from smithery.utils.url import encode_config_to_base64

        # Define what config your server accepts
        class ConfigSchema(BaseModel):
            api_key: str
            default_location: str = "New York"
            units: str = "celsius"

        app = from_fastmcp(FastMCP(), config_schema=ConfigSchema)

        @app.tool()
        def get_weather(location: str = None) -> str:
            config = app.get_context().session_config
            # Use user's config values
            loc = location or config.default_location
            return f"Weather in {loc}: 22°{config.units[0].upper()} (using API key: {config.api_key[:8]}...)"

        # User's session config is received via: POST /mcp?config=BASE64_JSON
        # Access validated config in your tools via ctx.session_config
        ```
    """
    return SmitheryFastMCP(fastmcp_instance, config_schema)




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
