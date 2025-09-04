"""
👋 Welcome to your Smithery project!
To run your server, run "uv run dev"

You might find these resources useful:

🧑‍💻 MCP's Python SDK (helps you define your server)
https://github.com/modelcontextprotocol/python-sdk

💻 smithery CLI (run "npx @smithery/cli dev" or explore other commands below)
https://smithery.ai/docs/concepts/cli
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from smithery import from_fastmcp
from smithery.server.fastmcp_patch import SmitheryFastMCP


# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    capitalize: bool = True  # Capitalize the greeting


def create_server(config: ConfigSchema) -> SmitheryFastMCP:
    """Create and configure the MCP server."""

    # Validate config at startup
    config = ConfigSchema.model_validate(config)

    server = from_fastmcp(
        FastMCP(name="Say Hello"),
        config_schema=ConfigSchema,
    )

    # Add a tool
    @server.tool()
    def hello(name: str) -> str:
        """Say hello to someone."""
        ctx = server.get_context()
        config = ctx.session_config  # Returns validated ConfigSchema instance

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


# Export for Smithery build system
default = create_server
config_schema = ConfigSchema


def main():
    """Main entry point to run the server with streamable HTTP transport."""
    import os

    # Create config instance with defaults
    config = ConfigSchema()

    # Create server instance
    server = create_server(config)

    # Get port from environment or default to 8081
    port = int(os.environ.get("PORT", "8081"))
    server.settings.port = port

    print(f"🚀 Starting MCP server on port {port}")
    print("📡 Using streamable HTTP transport")

    # Run with streamable HTTP transport
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
