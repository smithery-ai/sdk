"""
Smithery Decorators

Provides the @smithery decorator for streamlined MCP server creation.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from pydantic import BaseModel

from .server.fastmcp_patch import SmitheryFastMCP, from_fastmcp


def smithery(
    *,
    config_schema: type[BaseModel] | None = None
) -> Callable:
    """
    Decorator that enhances FastMCP servers with Smithery deployment features.

    Adds session-scoped configuration, CORS headers, and deployment patches
    to any FastMCP server you create.

    Args:
        config_schema: Optional Pydantic model for session configuration

    Usage:
        @smithery(config_schema=ConfigSchema)
        def create_server(config: ConfigSchema):
            # Create your FastMCP server as usual
            server = FastMCP("My Server")

            @server.tool()
            def my_tool() -> str:
                return "Hello!"

            return server

    Your function receives the validated config and should return a FastMCP instance.
    The decorator automatically enhances it for Smithery deployment.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(config: Any) -> SmitheryFastMCP:
            # Call user function - they create and configure their own FastMCP instance
            fastmcp_instance = func(config)

            # Apply Smithery enhancements to their FastMCP server
            return from_fastmcp(fastmcp_instance, config_schema=config_schema)

        # Store metadata on the wrapper function for discovery
        wrapper._smithery_config_schema = config_schema
        wrapper._smithery_decorator = True  # Flag to identify decorated functions

        return wrapper

    return decorator
