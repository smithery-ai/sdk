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

        Session config is parsed from URL parameters and validated against the provided schema.
        In practice, each session maintains consistent config throughout its lifecycle.

        Args:
            config_schema: Optional Pydantic model for session configuration.
                          Config parameters are received from URL query params on each request.

        Usage:
            # Server with configuration
            @smithery.server(config_schema=ConfigSchema)
            def create_server():
                server = FastMCP("My Server")

                @server.tool()
                def my_tool(arg: str, ctx: Context) -> str:
                    # Access session-specific config through context
                    session_config = ctx.session_config
                    return f"Hello {arg} with token {session_config.access_token}"

                return server

            # Server without configuration
            @smithery.server()
            def create_server():
                server = FastMCP("My Server")

                @server.tool()
                def my_tool(arg: str, ctx: Context) -> str:
                    # ctx.session_config will be an empty dict {}
                    return f"Hello {arg}"

                return server

        Your function creates and returns a FastMCP instance.
        Tools access session-scoped config via ctx.session_config (parsed from URL params).
        Each session maintains its own config, enabling per-user/per-session customization.
        The decorator automatically enhances it for Smithery deployment.
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(config: Any = None) -> SmitheryFastMCP:
                # Call user function without config - they access it via ctx.session_config in tools
                fastmcp_instance = func()

                # Apply Smithery enhancements to their FastMCP server
                return from_fastmcp(fastmcp_instance, config_schema=config_schema)

            # Store metadata on the wrapper function for discovery
            wrapper._smithery_config_schema = config_schema
            wrapper._smithery_decorator = True  # Flag to identify decorated functions

            return wrapper

        return decorator


# Create the main smithery instance that users will import
smithery = SmitheryDecorators()
