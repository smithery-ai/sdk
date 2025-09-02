"""
Example of using the stateless MCP server with FastMCP.

This example shows how to wrap a FastMCP server with the stateless server
for serverless environments and stateless API integrations.
"""

import uvicorn
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from smithery import create_stateless_server, StatelessServerOptions


# Define your config schema (optional)
class ConfigSchema(BaseModel):
    debug: bool = False
    api_key: str = ""
    max_requests: int = 100


def create_mcp_server() -> FastMCP:
    """Create your FastMCP server."""
    mcp = FastMCP("Stateless Example Server")

    @mcp.tool()
    def hello(name: str) -> str:
        """Say hello to someone."""
        return f"Hello, {name}!"

    @mcp.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return '"Hello, World" first appeared in a 1972 Bell Labs memo by Brian Kernighan.'

    @mcp.prompt()
    def greet(name: str) -> str:
        """Generate a greeting prompt."""
        return f"Say hello to {name}"

    return mcp


def main():
    """Run the stateless server."""
    # Create your FastMCP server
    mcp_server = create_mcp_server()
    
    # Configure the stateless server options
    options = StatelessServerOptions(
        config_schema=ConfigSchema  # Optional: validate config against this schema
    )
    
    # Create the stateless Starlette app
    app = create_stateless_server(mcp_server, options)
    
    # Run with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    main()
