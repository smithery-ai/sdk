"""
👋 Welcome to your Smithery project!
To run your server, use "uv run dev"
To test interactively, use "uv run playground"

You might find this resources useful:

🧑‍💻 MCP's Python SDK (helps you define your server)
https://github.com/modelcontextprotocol/python-sdk
"""

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from smithery.decorators import smithery


# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    # access_token: str = Field(..., description="Your access token for authentication")
    pirate_mode: bool = Field(False, description="Speak like a pirate")


# For servers with configuration:
@smithery.server(config_schema=ConfigSchema)
# For servers without configuration, simply use:
# @smithery.server()
def create_server():
    """Create and configure the MCP server."""

    # Create your FastMCP server as usual
    server = FastMCP("Say Hello")

    # Add a tool
    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """Say hello to someone."""
        # Access session-specific config through context
        session_config = ctx.session_config

        # In real apps, use token for API requests:
        # requests.get(url, headers={"Authorization": f"Bearer {session_config.access_token}"})
        # if not session_config.access_token:
        #     return "Error: Access token required"

        # Create greeting based on pirate mode
        if session_config.pirate_mode:
            return f"Ahoy, {name}!"
        else:
            return f"Hello, {name}!"

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
