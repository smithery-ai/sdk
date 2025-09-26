"""
Smithery Session Config Middleware

This module provides middleware for handling session configuration and validation.
"""

import logging
from urllib.parse import parse_qsl

from pydantic import BaseModel, ValidationError  # type: ignore
from starlette.responses import JSONResponse  # type: ignore

from ..utils.config import parse_config_from_asgi_scope
from ..utils.responses import create_error_response, get_config_schema_dict


class SessionConfigMiddleware:
    """Extract config from URL parameters and validate with schema."""

    def __init__(self, app, config_schema: type[BaseModel] | None = None):
        self.app = app
        self.config_schema = config_schema

    def _get_reserved_params_in_query(self, scope) -> list[str]:
        """Check for reserved parameters in query string that are not config keys."""
        reserved = {"api_key", "profile"}
        query = scope.get("query_string", b"").decode("utf-8")
        pairs = parse_qsl(query, keep_blank_values=True)

        def is_config_key(k: str) -> bool:
            return k.startswith("config.") or k.startswith("config[")

        return [k for (k, _v) in pairs if k in reserved and not is_config_key(k)]

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

        # Check for reserved parameters first (deterministic policy)
        reserved_params_in_query = self._get_reserved_params_in_query(scope)
        if reserved_params_in_query:
            # User tried to use reserved parameters - give helpful error
            error_response = create_error_response(
                400,
                "Reserved parameters not allowed in config",
                f"The following parameters are reserved and cannot be used in session config: {', '.join(reserved_params_in_query)}. "
                f"These parameters are used by Smithery internally and should not be included in your configuration schema.",
                instance="/mcp"
            )
            await error_response(scope, receive, send)
            return

        # Parse config from URL parameters and store in scope
        try:
            raw_config = parse_config_from_asgi_scope(scope)

            # Validate and create ConfigSchema instance
            if self.config_schema:
                try:
                    config_instance = self.config_schema(**raw_config)
                    # Normalize to dict for consistent access
                    scope["session_config"] = config_instance.model_dump()
                except ValidationError as e:
                    # Normal validation error
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
                scope["session_config"] = raw_config

        except ValueError as e:
            # Config parsing failed - return 400 error
            if "config" in str(e).lower():
                error_response = create_error_response(400, "Invalid config", str(e))
                await error_response(scope, receive, send)
                return
            raise
        except Exception as e:
            # Log unexpected errors and return 500
            logger = logging.getLogger(__name__)
            logger.exception(f"Unexpected error processing session config: {e}")

            error_response = create_error_response(
                500,
                "Internal server error",
                "Failed to process session configuration"
            )
            await error_response(scope, receive, send)
            return

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
                }
            )

            await response(scope, receive, send)

        except Exception:
            # Send error response using Starlette
            error_response = JSONResponse(
                content={"error": "Internal server error"},
                status_code=500,
            )
            await error_response(scope, receive, send)
