"""
Smithery Decorators

Provides decorators for streamlined MCP server creation and deployment.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from pydantic import BaseModel

from .server.fastmcp_patch import SmitheryFastMCP, from_fastmcp


class SmitheryDecorators:
    """
    Smithery decorator namespace for extensible server creation.

    Provides decorators like @smithery.server() for different aspects
    of MCP server creation and deployment.
    """

    @staticmethod
    def server(
        *,
        config_schema: type[BaseModel] | None = None
    ) -> Callable:
        """
        Decorator that enhances FastMCP servers with Smithery deployment features.

        Adds session-scoped configuration, CORS headers, and deployment patches
        to any FastMCP server you create.

        Args:
            config_schema: Optional Pydantic model for session configuration.
                          If None, the server function will receive an empty dict.

        Usage:
            # Server with configuration
            @smithery.server(config_schema=ConfigSchema)
            def create_server(config: ConfigSchema):
                server = FastMCP("My Server")

                @server.tool()
                def my_tool(ctx, arg: str) -> str:
                    # Access session-specific config through context
                    session_config = ctx.session_config
                    return f"Hello {arg} with token {session_config.access_token}"

                return server

            # Server without configuration
            @smithery.server()
            def create_server(config):
                server = FastMCP("My Server")

                @server.tool()
                def my_tool(ctx, arg: str) -> str:
                    # ctx.session_config will be an empty dict {}
                    return f"Hello {arg}"

                return server

        Your function receives the validated config and should return a FastMCP instance.
        Tools access session-specific config via ctx.session_config.
        The decorator automatically enhances it for Smithery deployment.
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(config: Any) -> SmitheryFastMCP:
                # If no config schema, pass empty dict to keep the interface consistent
                if config_schema is None:
                    config = {}

                # Call user function - they create and configure their own FastMCP instance
                fastmcp_instance = func(config)

                # Apply Smithery enhancements to their FastMCP server
                return from_fastmcp(fastmcp_instance, config_schema=config_schema)

            # Store metadata on the wrapper function for discovery
            wrapper._smithery_config_schema = config_schema
            wrapper._smithery_decorator = True  # Flag to identify decorated functions

            return wrapper

        return decorator


# Create the main smithery instance that users will import
smithery = SmitheryDecorators()
