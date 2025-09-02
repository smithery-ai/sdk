"""
🚀 Patched FastMCP Demo - Native Session Config Support!

This demonstrates the revolutionary new API where config gets automatically
injected into your tools with full type safety and session scoping.
"""

import json
from pydantic import BaseModel
from smithery.server.patched_fastmcp import PatchedFastMCP


# Define your config schema with full type safety
class ServerConfig(BaseModel):
    debug: bool = False
    api_key: str = "default-key"
    max_requests: int = 100
    environment: str = "development"
    features: list[str] = []


def main():
    """Demo the patched FastMCP with automatic config injection."""
    
    # 🎉 Create FastMCP with native session config support!
    server = PatchedFastMCP(
        name="Patched Demo Server",
        session_config_schema=ServerConfig  # ✨ Magic happens here!
    )

    # 🚀 Config gets automatically injected based on parameter type!
    @server.tool()
    def greet_user(name: str, config: ServerConfig) -> str:
        """Greet a user with config-aware behavior."""
        if config.debug:
            return f"[DEBUG] Hello {name}! (API: {config.api_key}, Env: {config.environment})"
        return f"Hello {name}!"

    @server.tool()
    def check_limits(requests: int, config: ServerConfig) -> str:
        """Check if request count is within limits."""
        if requests > config.max_requests:
            return f"❌ Limit exceeded! {requests} > {config.max_requests}"
        return f"✅ Within limits: {requests}/{config.max_requests}"

    @server.tool()
    def feature_status(feature: str, config: ServerConfig) -> str:
        """Check if a feature is enabled."""
        if feature in config.features:
            return f"✅ Feature '{feature}' is enabled"
        return f"❌ Feature '{feature}' is not enabled"

    @server.tool()
    def environment_info(config: ServerConfig) -> str:
        """Get current environment information."""
        return f"""
🌍 Environment: {config.environment}
🔧 Debug Mode: {config.debug}
🔑 API Key: {config.api_key[:8]}...
📊 Max Requests: {config.max_requests}
🎯 Features: {', '.join(config.features) if config.features else 'None'}
        """.strip()

    # 🎯 Alternative: Use context to access config
    @server.tool()
    def session_info(user: str) -> str:
        """Get session info using context."""
        ctx = server.get_context()
        config = ctx.session_config  # 🆕 Built into context!
        
        return f"""
👋 Hello {user}!
📍 Session Config: {json.dumps(config, indent=2)}
        """.strip()

    # 🎨 Resources can also use config injection
    @server.resource("config://current")
    def current_config() -> str:
        """Show current session configuration."""
        ctx = server.get_context()
        config = ctx.session_config
        return json.dumps(config, indent=2)

    @server.resource("status://server")  
    def server_status() -> str:
        """Server status with config context."""
        ctx = server.get_context()
        config = ctx.session_config
        
        status = {
            "server": "Patched FastMCP Demo",
            "environment": config.get("environment", "unknown"),
            "debug_mode": config.get("debug", False),
            "features_count": len(config.get("features", []))
        }
        return json.dumps(status, indent=2)

    # 🎭 Prompts with config support
    @server.prompt()
    def analyze_request(task: str, config: ServerConfig) -> list:
        """Generate analysis prompt based on config."""
        messages = [
            {
                "role": "user", 
                "content": f"Analyze this task: {task}"
            }
        ]
        
        if config.debug:
            messages.append({
                "role": "system",
                "content": f"Debug mode active. Environment: {config.environment}"
            })
        
        return messages

    # 🎪 Show off the beautiful new API
    print("🚀 Starting Patched FastMCP Demo Server!")
    print("✨ Features:")
    print("  • Automatic config injection into tools")
    print("  • Type-safe configuration with Pydantic")
    print("  • Session-scoped config (parsed once per session)")
    print("  • Enhanced Context with session_config property")
    print("  • Zero middleware setup required!")
    print()
    print("📝 Try these config examples:")
    print("  ?debug=true&api_key=prod123&environment=production")
    print("  ?debug=false&max_requests=500&features=[\"cache\",\"analytics\"]")
    print()
    
    # Run on a different port to avoid conflicts
    server.settings.port = 8001
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
