"""
🚀 Welcome to your Smithery project!

To run your server: uv run python -m src.server
"""

from pydantic import BaseModel
from smithery.server.patched_fastmcp import PatchedFastMCP
from mcp.server.fastmcp import Context


# Define your config schema
class ConfigSchema(BaseModel):
    access_token: str = ""


def main():
    """Create and run the MCP server with native session config support."""
    
    
    server = PatchedFastMCP(
        name="Say Hello Server",
        config_schema=ConfigSchema
    )

    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """Say hello to someone."""
        config = ctx.session_config
        access_token = config.get('access_token', '')
        
        if access_token:
            return f"Hello {name}! (Authenticated with token: {access_token[:8]}...)"
        return f"Hello, {name}!"

    @server.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return '"Hello, World" first appeared in a 1972 Bell Labs memo by Brian Kernighan.'

    @server.prompt()
    def greet(name: str) -> list:
        """Generate a greeting prompt."""
        return [{"role": "user", "content": f"Say hello to {name}"}]

    # Run the server!
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()