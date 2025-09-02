"""
🚀 Welcome to your Smithery project!
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from smithery import from_fastmcp


# Optional: If you have user-level config, define it here
# This should map to the config in your smithery.yaml file
class ConfigSchema(BaseModel):
    capitalize: bool = True  # Capitalize the greeting


def create_server(config: ConfigSchema) -> FastMCP:
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
        config = ctx.session_config
        
        # Apply capitalization based on config
        display_name = name.upper() if config.get("capitalize", True) else name.lower()
        greeting = f"Hello, {display_name}!"
        
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


def main():
    """Main entry point."""
    # In a real app, you'd get config from smithery.yaml
    config = ConfigSchema()
    server = create_server(config)
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
