"""
FastMCP + Smithery Demo

Shows how to use session config.
"""

import json
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from smithery import from_fastmcp


class ServerConfig(BaseModel):
    debug: bool = False
    api_key: str = "default-key"
    max_requests: int = 100
    environment: str = "development"
    features: list[str] = []


def main():
    server = from_fastmcp(
        FastMCP(name="Demo Server"),
        config_schema=ServerConfig
    )
    @server.tool()
    def greet_user(name: str, config: ServerConfig) -> str:
        """Greet a user."""
        if config.debug:
            return f"[DEBUG] Hello {name}! (API: {config.api_key}, Env: {config.environment})"
        return f"Hello {name}!"

    @server.tool()
    def check_limits(requests: int, config: ServerConfig) -> str:
        """Check if request count is within limits."""
        if requests > config.max_requests:
            return f"Limit exceeded! {requests} > {config.max_requests}"
        return f"Within limits: {requests}/{config.max_requests}"

    @server.resource("config://current")
    def current_config() -> str:
        """Show current session configuration."""
        ctx = server.get_context()
        config = ctx.session_config
        return json.dumps(config, indent=2)

    @server.prompt()
    def analyze_request(task: str, config: ServerConfig) -> list:
        """Generate analysis prompt."""
        messages = [{"role": "user", "content": f"Analyze this task: {task}"}]
        
        if config.debug:
            messages.append({
                "role": "system",
                "content": f"Debug mode active. Environment: {config.environment}"
            })
        
        return messages

    print("Starting demo server...")
    print("Try: ?debug=true&api_key=prod123&environment=production")
    
    # Run on a different port to avoid conflicts
    server.settings.port = 8001
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
