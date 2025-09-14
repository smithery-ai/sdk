# AGENTS.md

Welcome to the **Smithery Python MCP Server Scaffold**!

This is the template project that gets cloned when you run `uvx smithery init`. It provides everything you need to build, test, and deploy a Model Context Protocol (MCP) server with Smithery.

## What's Included

- **FastMCP Server** with Smithery session-scoped configuration support
- **Example Tool** (`hello` tool with pirate mode configuration)
- **Example Resource** (`history://hello-world` with Hello World origin story)
- **Example Prompt** (`greet` prompt for generating greeting messages)
- **Development Workflow** (`uv run dev` for local testing, `uv run playground` for interactive testing)
- **Deployment Ready** configuration for the Smithery platform
- **Session Management** via `@smithery.server()` decorator with optional config schemas

## Quick Start Commands

```bash
# Run development server (streamable HTTP on port 8081)
uv run dev

# Test with interactive playground
uv run playground
```

## Development Workflow

Based on the [Model Context Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture.md), MCP servers provide three core primitives:

### 1. Tools (for actions)
Add executable functions that AI applications can invoke to perform actions:

```python
@server.tool()
def hello(name: str, ctx: Context) -> str:
    """Say hello to someone."""
    session_config = ctx.session_config
    if session_config.pirate_mode:
        return f"Ahoy, {name}!"
    else:
        return f"Hello, {name}!"
```

### 2. Resources (for static data) 
Add data sources that provide contextual information:

```python
@server.resource("history://hello-world")
def hello_world() -> str:
    """The origin story of the famous 'Hello, World' program."""
    return (
        '"Hello, World" first appeared in a 1972 Bell Labs memo by '
        "Brian Kernighan and later became the iconic first program "
        "for beginners in countless languages."
    )
```

### 3. Prompts (for interaction templates)
Add reusable templates that help structure interactions:

```python
@server.prompt()
def greet(name: str) -> list:
    """Generate a greeting prompt."""
    return [
        {
            "role": "user",
            "content": f"Say hello to {name}",
        },
    ]
```

### Project Structure

```
your-server/
├── pyproject.toml         # Project config with [tool.smithery] section
├── smithery.yaml          # Runtime specification (runtime: python)
├── src/
│   └── hello_server/      # Your server module (rename this!)
│       ├── __init__.py
│       └── server.py      # Main server implementation
└── README.md
```

### Customizing Your Project

**Important:** You'll want to rename `hello_server` to match your actual project:

1. **Rename the module directory:**
   ```bash
   mv src/hello_server src/your_project_name
   ```

2. **Update pyproject.toml:**
   ```toml
   [project]
   name = "your-project-name"
   
   [tool.smithery]
   server = "your_project_name.server:create_server"  # Points to your server function
   ```

3. **Update imports in your code:**
   ```bash
   # Test your renamed server works
   uv run python -c "from your_project_name.server import create_server; print(create_server())"
   ```

**Note:** The function name `create_server` can be anything you want - just make sure the `[tool.smithery]` server path matches your actual function name (e.g., `"module:my_function_name"`).

## Session Configuration

Session configuration allows clients to connect to your MCP server with personalized settings. Think of it like user preferences - each connection gets its own configuration that doesn't affect other sessions, perfect for passing API keys, customizing behavior, and personalizing responses.

When you define a configuration schema, Smithery automatically:
- **Generates a configuration UI** with form elements (text inputs, dropdowns, checkboxes)
- **Passes configurations to your server** as URL parameters  
- **Shows helpful descriptions** as form labels and tooltips
- **Applies default values** and enforces required fields

This is accessed through the FastMCP `Context` object in your tools and resources.

### Real-World Example: Weather Server

Let's say you're building a weather server. You might want users to customize their preferred temperature unit, provide an API key, or set their default location:

```python
class WeatherConfig(BaseModel):
    api_key: str = Field(..., description="Your OpenWeatherMap API key")
    temperature_unit: str = Field("celsius", description="Temperature unit (celsius/fahrenheit)")
    default_location: str = Field("New York", description="Default city for weather queries")

@smithery.server(config_schema=WeatherConfig)
def create_weather_server():
    # Your weather tools use ctx.session_config.api_key, ctx.session_config.temperature_unit, etc.
```

**Usage scenarios:**
- **User A**: API key `abc123`, prefers Fahrenheit, lives in San Francisco
- **User B**: API key `xyz789`, prefers Celsius, lives in Singapore

Each user gets personalized weather data without affecting others.

### Understanding Context

The `Context` object is automatically injected into tool and resource functions via type hints. In Smithery, it includes session-specific configuration:

```python
from mcp.server.fastmcp import Context

@server.tool()
def my_tool(name: str, ctx: Context) -> str:
    """Tool that uses session config."""
    # Access session-specific config
    config = ctx.session_config
    
    # Use config values (API keys, preferences, etc.)
    if config.debug:
        return f"DEBUG: Hello {name}"
    return f"Hello {name}"
```

### How Session Config Works

1. **Define config schema** (optional):
```python
class ConfigSchema(BaseModel):
    # Required field - users must provide this
    api_key: str = Field(..., description="Your API key")
    
    # Optional fields with defaults - users can customize or use defaults
    debug: bool = Field(False, description="Debug mode")
    max_results: int = Field(10, description="Maximum results to return")
    
    # Optional field without default - can be None
    custom_endpoint: str | None = Field(None, description="Custom API endpoint")

@smithery.server(config_schema=ConfigSchema)
def create_server():
    # Your server setup
```

**Field Types:**
- **Required**: Use `Field(...)` - users must provide a value
- **Optional with default**: Use `Field(default_value)` - users can customize or use the default
- **Optional without default**: Use `Field(None)` with nullable type - completely optional

2. **Pass config via URL parameters**:
```
http://localhost:8000/mcp?api_key=xyz123&debug=true
```

3. **Each session gets isolated config**:
- Session A: `debug=true, api_key=xyz123`
- Session B: `debug=false, api_key=abc456`
- Sessions don't interfere with each other

### Why This Matters

- **Multi-user support**: Different users can have different API keys/settings
- **Environment isolation**: Dev/staging/prod configs per session
- **Security**: API keys stay session-scoped, not server-global

### Secure Config Distribution (Production)

In production, Smithery handles sensitive configuration securely:

1. **Users save config in Smithery** (API keys, tokens, etc.)
2. **OAuth authentication** is built-in - no manual key management
3. **Smithery Gateway** securely forwards config to your server
4. **Your server receives config** via `ctx.session_config` as usual

**The flow:**
```
User → Smithery Platform → Gateway (OAuth) → Your Server
     (saves config)    (secure forwarding)   (receives config)
```

**Benefits:**
- Users never expose sensitive keys directly to your server
- OAuth handles authentication automatically
- Config is encrypted in transit through the gateway
- You focus on your server logic, not security infrastructure

### Testing Your Server

There are two main ways to test your MCP server:

#### Method 1: Smithery Playground
```bash
uv run playground         # Actually runs: uv run smithery playground
```
This opens the Smithery Playground in your browser with your local server tunneled through ngrok. Perfect for interactive testing and seeing your tools in action.

**Note**: If using `--reload` mode, you'll need to refresh the playground to start a new session after code changes.

#### Method 2: Direct MCP Protocol Testing
```bash
# Start server (with optional reload for development)
uv run dev                # Actually runs: uv run smithery dev
uv run dev --reload       # Auto-reload on code changes
```

**Complete MCP Testing Workflow:**
1. Start server: `uv run dev` (runs on port 8081 by default)
2. Initialize with config (always include config params): 
```bash
curl -X POST "http://127.0.0.1:8081/mcp?pirate_mode=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```
3. Get session ID from server logs: "Created new transport with session ID: [uuid]"
4. Send notifications/initialized with session header:
```bash
curl -X POST "http://127.0.0.1:8081/mcp?pirate_mode=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: [session-id]" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```
5. Test the hello tool with pirate mode:
```bash
curl -X POST "http://127.0.0.1:8081/mcp?pirate_mode=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: [session-id]" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"hello","arguments":{"name":"World"}}}'
```
Expected response: `"Ahoy, World!"` (with pirate_mode=true) or `"Hello, World!"` (with pirate_mode=false)


### Deployment Configuration

**pyproject.toml:**
```toml
[tool.smithery]
server = "my_server.server:create_server"  # Points to your @smithery.server() function

[project.scripts]
dev = "smithery.cli.dev:main"              # Development server
playground = "smithery.cli.playground:main" # Interactive testing
```

## Deployment & CI/CD

### Local Deployment
```bash
# Python server deployment prep
uv build                   # Creates wheel in dist/
git add . && git commit -m "Deploy ready"
git push origin main
```

### Production Deployment
1. Push code to GitHub repository
2. Deploy via [smithery.ai/new](https://smithery.ai/new)
3. Smithery handles containerization and hosting
4. **Automatic Registry Mirroring**: Your server gets published to both the Smithery platform and the official MCP registry for better discoverability

## Architecture Notes

### Key Dependencies
- **mcp>=1.13.1**: Model Context Protocol SDK with CLI tools
- **smithery>=0.1.24**: Smithery enhancements for session config and deployment
- **Python >=3.10**: Required Python version

### Security Considerations
- Session-scoped API keys and configuration
- CORS headers for web client compatibility
- Request logging and monitoring via gateway
- Authentication handled by Smithery platform

## Pre-Deployment Checklist

Before deploying, ensure your server works locally:

### 1. Basic Server Test
```bash
# This should start your server on localhost:8081
uv run dev
```

**Common issues:**
- **"Module not found"**: Run `uv sync` first
- **"Server function not callable"**: Check your `[tool.smithery]` server reference in `pyproject.toml`
- **"Config schema errors"**: Verify your Pydantic model can be instantiated

### 2. Validate Server Creation
```bash
# Test that your server function works (replace with your actual module name)
uv run python -c "from your_project_name.server import create_server; print(create_server())"
```

**Expected output:** Should print something like `<smithery.server.fastmcp_patch.SmitheryFastMCP object at 0x...>` without errors. If you see import errors or exceptions, check your server configuration.

### 3. Test with Playground
```bash
# This should open playground in your browser
uv run playground
```

**Expected behavior:** Browser opens with Smithery Playground connected to your local server.

## Troubleshooting

### Port Issues
- Default port is **8081** (not 8000)
- Change with: `uv run dev --port 8000`
- Kill existing process: `lsof -ti:8081 | xargs kill`

### Config Issues
```bash
# Check your pyproject.toml configuration
cat pyproject.toml | grep -A5 "tool.smithery"

# Should show:
# [tool.smithery]
# server = "hello_server.server:create_server"
```

### Import Issues
- Ensure you're in the project root directory
- Run `uv sync` to install dependencies
- Check that your server module path matches the `[tool.smithery]` reference

## Resources

- **Documentation**: [smithery.ai/docs](https://smithery.ai/docs)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Python Quickstart**: [smithery.ai/docs/getting_started/quickstart_build_python.md](https://smithery.ai/docs/getting_started/quickstart_build_python.md)
- **GitHub**: [github.com/smithery-ai/sdk](https://github.com/smithery-ai/sdk)
- **Registry**: [smithery.ai](https://smithery.ai) for discovering and deploying MCP servers
