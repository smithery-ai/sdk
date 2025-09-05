"""
👋 Welcome to your Smithery project!
To run your server, use "uv run dev"
To test interactively, use "uv run playground"

You might find this resources useful:

🧑‍💻 MCP's Python SDK (helps you define your server)
https://github.com/modelcontextprotocol/python-sdk
"""

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

from smithery.decorators import smithery


# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    access_token: str = Field(..., description="Your access token for authentication")
    capitalize: bool = Field(True, description="Whether to capitalize the greeting")


@smithery(config_schema=ConfigSchema)
def create_server(config: ConfigSchema):
    """Create and configure the MCP server."""
    
    # Create your FastMCP server as usual
    server = FastMCP("Say Hello")

    # Add a tool
    @server.tool()
    def hello(name: str) -> str:
        """Say hello to someone."""
        # Verify access token is provided (it's required, so should always be present)
        if not config.access_token:
            return "Error: Access token required"

        # Apply capitalization to the entire greeting based on config
        base_greeting = f"Hello, {name}!"
        greeting = base_greeting.upper() if config.capitalize else base_greeting.lower()

        return greeting

    # Add a resource
    @server.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return (
            '"Hello, World" first appeared in a 1972 Bell Labs memo by '
            "Brian Kernighan and later became the iconic first program "
            "for beginners in countless languages."
        )

    # Add a prompt
    @server.prompt()
    def greet(name: str) -> list:
        """Generate a greeting prompt."""
        return [
            {
                "role": "user",
                "content": f"Say hello to {name}",
            },
        ]

    return server
