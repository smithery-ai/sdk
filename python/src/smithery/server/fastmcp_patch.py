"""
Smithery FastMCP Patch - Session Config Support

This provides a wrapper for FastMCP that adds middleware for smithery session config and CORS.
"""

from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from ..utils.config import parse_config_from_asgi_scope
from ..utils.responses import create_error_response, get_config_schema_dict


class SmitheryFastMCP:
    """Wrapper that adds session config and CORS to FastMCP."""

    def __init__(self, fastmcp_instance: FastMCP, config_schema: type[BaseModel] | None = None):
        self._fastmcp = fastmcp_instance
        self._config_schema = config_schema

        # Patch the instance methods
        self._patch_streamable_http_app()

    def __getattr__(self, name: str):
        """Forward attribute access to wrapped FastMCP instance."""
        # First check if the attribute exists on the wrapped instance
        if hasattr(self._fastmcp, name):
            attr = getattr(self._fastmcp, name)

            # If it's a callable (method), return it directly
            # Python will handle the binding automatically
            return attr

        # If attribute doesn't exist on wrapped instance, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _patch_streamable_http_app(self):
        """Add CORS and session config middleware to StreamableHTTP app."""
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
    """Extract config from URL parameters and validate with schema."""

    def __init__(self, app, config_schema=None):
        self.app = app
        self.config_schema = config_schema

    async def __call__(self, scope, receive, send):
        # Handle well-known config schema endpoint
        if (scope["type"] == "http" and
            scope["method"] == "GET" and
            scope["path"] == "/.well-known/mcp-config"):
            await self._handle_config_schema_endpoint(scope, receive, send)
            return

        # Only process HTTP requests to MCP endpoint
        if scope["type"] != "http" or scope["method"] != "POST" or scope["path"] != "/mcp":
            await self.app(scope, receive, send)
            return

        # Parse config from URL parameters and store in scope
        try:
            raw_config = parse_config_from_asgi_scope(scope)

            # Validate and create ConfigSchema instance
            if self.config_schema:
                try:
                    config_instance = self.config_schema(**raw_config)
                except ValidationError as e:
                    # Return 422 for any validation issues
                    # (missing required fields or invalid values)
                    config_schema_dict = get_config_schema_dict(self.config_schema)
                    error_response = create_error_response(
                        422,
                        "Invalid configuration parameters",
                        "One or more config parameters are invalid.",
                        e,
                        config_schema_dict,
                        instance="/mcp"
                    )
                    await error_response(scope, receive, send)
                    return
            else:
                # No schema, store raw dict
                config_instance = raw_config

            # Store validated config instance in scope
            scope["session_config"] = config_instance

        except ValueError as e:
            # Config parsing failed - return 400 error
            if "config" in str(e).lower():
                error_response = create_error_response(400, "Invalid config", str(e))
                await error_response(scope, receive, send)
                return
            raise
        except Exception:
            # Other unexpected errors - use default config for backward compatibility
            config_instance = self.config_schema() if self.config_schema else {}
            scope["session_config"] = config_instance

        await self.app(scope, receive, send)

    async def _handle_config_schema_endpoint(self, scope, receive, send):
        """Handle GET /.well-known/mcp-config endpoint."""
        headers = {k.decode('utf-8'): v.decode('utf-8') for k, v in scope.get('headers', [])}
        host_header = headers.get('host', f"{scope['server'][0]}:{scope['server'][1]}")

        try:
            if self.config_schema:
                base_schema = get_config_schema_dict(self.config_schema)

                # Add proper JSON Schema metadata to match TypeScript implementation
                # Use Host header like TypeScript SDK instead of internal server address
                host = host_header

                config_schema_dict = {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "$id": f"{scope['scheme']}://{host}/.well-known/mcp-config",
                    "title": "MCP Session Configuration",
                    "description": "Schema for the /mcp endpoint configuration",
                    "x-query-style": "dot+bracket",
                    **base_schema,
                }

                response_data = config_schema_dict
            else:
                response_data = {"message": "No configuration schema available"}

            # Use Starlette's JSONResponse for proper HTTP handling
            response = JSONResponse(
                content=response_data,
                status_code=200,
                headers={
                    "content-type": "application/schema+json; charset=utf-8",  # Match TypeScript exactly
                    "cache-control": "no-cache, no-store, must-revalidate",  # Prevent Fly.io caching/transformation
                    "access-control-allow-origin": "*",
                }
            )

            await response(scope, receive, send)

        except Exception:
            # Send error response using Starlette
            error_response = JSONResponse(
                content={"error": "Internal server error"},
                status_code=500,
                headers={
                    "access-control-allow-origin": "*",
                }
            )
            await error_response(scope, receive, send)


def from_fastmcp(
    fastmcp_instance: FastMCP,
    *,
    config_schema: type[BaseModel] | None = None
) -> SmitheryFastMCP:
    """Add session config support and CORS to FastMCP. Config accessed via ctx.session_config."""
    return SmitheryFastMCP(fastmcp_instance, config_schema)




# Patch the Context class to include session config
def patch_context_with_session_config():
    """Add session_config property to FastMCP Context class."""

    @property
    def session_config(self) -> Any:
        """Get session config from request scope."""
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
