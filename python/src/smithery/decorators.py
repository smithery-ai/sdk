"""
Smithery Decorators

Provides the @smithery decorator for streamlined MCP server creation.
"""

from typing import Any, Callable, Optional
from functools import wraps

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from .server.fastmcp_patch import from_fastmcp, SmitheryFastMCP


def smithery(
    *,
    config_schema: Optional[type[BaseModel]] = None,
    name: str = "MCP Server",
    description: Optional[str] = None
) -> Callable:
    """
    Decorator that creates a Smithery-patched MCP server with automatic configuration.
    
    Args:
        config_schema: Optional Pydantic model for session configuration
        name: Server name (default: "MCP Server")
        description: Optional server description
    
    Usage:
        @smithery(config_schema=ConfigSchema, name="My Server")
        def create_server(server, config: ConfigSchema):
            @server.tool()
            def my_tool() -> str:
                return "Hello!"
    
    The decorated function receives:
        - server: FastMCP instance to configure
        - config: Validated config instance (or dict if no schema)
    
    Returns a SmitheryFastMCP instance ready for deployment.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(config: Any) -> SmitheryFastMCP:
            # Create base FastMCP instance
            fastmcp_instance = FastMCP(name=name)
            
            # Set description if provided
            if description:
                # FastMCP doesn't have a direct description field, but we can add it as metadata
                fastmcp_instance._description = description
            
            # Call user function to configure the server
            # User function should configure tools, resources, prompts on the server
            result = func(fastmcp_instance, config)
            
            # Apply Smithery patches automatically
            # The result should be None (user modified server in-place) or the server instance
            server_to_wrap = result if result is not None else fastmcp_instance
            
            return from_fastmcp(server_to_wrap, config_schema=config_schema)
        
        # Store metadata on the wrapper function for discovery
        wrapper._smithery_config_schema = config_schema
        wrapper._smithery_name = name
        wrapper._smithery_description = description
        wrapper._smithery_decorator = True  # Flag to identify decorated functions
        
        return wrapper
    
    return decorator
