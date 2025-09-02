"""
🚀 Simple Patched FastMCP Demo - Just Hello Tool!

"""

from pydantic import BaseModel
from smithery.server.patched_fastmcp import PatchedFastMCP
from mcp.server.fastmcp import Context


# Define your config schema
class ConfigSchema(BaseModel):
    capitalize: bool = False


def main():
    """Simple demo with just one hello tool."""
    
    # Create FastMCP with native session config support
    server = PatchedFastMCP(
        name="Hello Server",
        config_schema=ConfigSchema
    )

    # Single tool with proper FastMCP Context injection!
    @server.tool()
    def hello(user: str, ctx: Context) -> str:
        """Say hello to a user."""
        
        # Access session config via injected context
        config = ctx.session_config
        
        greeting = "Hello"
        
        # Apply capitalization if enabled via session config
        if config.get('capitalize', False):
            return f"{greeting.upper()} {user.upper()}!"
        else:
            return f"{greeting} {user}!"

    # Run on port 8002
    server.settings.port = 8002
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
