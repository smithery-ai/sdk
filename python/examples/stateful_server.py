"""
Example of using the stateful MCP server with FastMCP.

This example shows how to wrap a FastMCP server with the stateful server
to handle session management and HTTP transport.
"""

import uvicorn
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from smithery import create_stateful_server, StatefulServerOptions, get_config_value, get_session_config, get_current_session_id


# Define your config schema (optional)
class ConfigSchema(BaseModel):
    debug: bool = False
    api_key: str = ""
    max_requests: int = 100


def main():
    """Run the stateful server."""
    # Create your FastMCP server
    mcp = FastMCP("Example Server")

    @mcp.tool()
    def hello(name: str) -> str:
        """Say hello to someone."""
        # Get config values from current request
        debug = get_config_value("debug", False)
        api_key = get_config_value("api_key", "")
        
        if debug:
            return f"Hello (DEBUG MODE), {name}! API Key: {api_key}"
        return f"Hello, {name}!"

    @mcp.tool()
    def get_config() -> str:
        """Show the current session's configuration."""
        session_id = get_current_session_id()
        config = get_session_config()
        return f"Session {session_id[:8] if session_id else 'unknown'} config: {config}"
    
    @mcp.tool()
    def get_session_info() -> str:
        """Get information about the current session."""
        session_id = get_current_session_id()
        return f"Current session ID: {session_id}"

    @mcp.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return '"Hello, World" first appeared in a 1972 Bell Labs memo by Brian Kernighan.'

    @mcp.prompt()
    def greet(name: str) -> str:
        """Generate a greeting prompt."""
        return f"Say hello to {name}"
    
    # Configure the stateful server options
    options = StatefulServerOptions(
        config_schema=ConfigSchema  # Optional: validate config against this schema
    )
    
    # Create the stateful Starlette app with middleware
    app = create_stateful_server(mcp, options)
    
    # Run with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
