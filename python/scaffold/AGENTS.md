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

# Run production server (optimized for deployment)
uv run start

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
    weather_api_key: str = Field(..., description="Your OpenWeatherMap API key")  # Note: 'api_key' is reserved
    temperature_unit: str = Field("celsius", description="Temperature unit (celsius/fahrenheit)")
    default_location: str = Field("New York", description="Default city for weather queries")

@smithery.server(config_schema=WeatherConfig)
def create_weather_server():
    # Your weather tools use ctx.session_config.weather_api_key, ctx.session_config.temperature_unit, etc.
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
    user_api_key: str = Field(..., description="Your API key")  # Note: avoid 'api_key' (reserved)
    
    # Optional fields with defaults - users can customize or use defaults
    debug: bool = Field(False, description="Debug mode")
    max_results: int = Field(10, description="Maximum results to return")
    
    # Optional field without default - can be None
    custom_endpoint: str | None = Field(None, description="Custom API endpoint")

@smithery.server(config_schema=ConfigSchema)
def create_server():
    # Your server setup
```

**Important:** Avoid using reserved parameter names (`api_key`, `profile`, `config`) in your schema fields. These are handled internally by Smithery.

**Field Types and Validation Behavior:**

- **Required Fields**: Use `Field(...)` - Server returns 422 error if missing
  ```python
  api_key: str = Field(..., description="Your API key")
  # Missing this field → 422 error with config schema
  ```

- **Optional with Default**: Use `Field(default_value)` - Uses default if not provided
  ```python
  debug: bool = Field(False, description="Debug mode")
  max_results: int = Field(10, description="Maximum results")
  # Missing these fields → Uses defaults (debug=False, max_results=10)
  ```

- **Optional without Default**: Use `Field(None)` with nullable type - Can be None
  ```python
  custom_endpoint: str | None = Field(None, description="Custom API endpoint")
  # Missing this field → Sets to None, no validation error
  ```

**Validation Logic:**
- **No config provided** → Uses defaults for optional fields, 422 only if required fields exist
- **Partial config** → Uses provided values + defaults for missing optional fields
- **Missing required fields** → 422 error with validation details and config schema
- **Invalid values** → 422 error (wrong types, constraint violations, etc.)

2. **Pass config via URL parameters**:
```
http://localhost:8000/mcp?user_api_key=xyz123&debug=true
```

**Reserved Parameters:**
The following parameter names are reserved and cannot be used in your configuration schema:
- `api_key` - Reserved for API key handling
- `profile` - Reserved for profile management  
- `config` - Reserved for internal configuration handling

Use alternative names for your configuration fields (e.g., `user_api_key`, `service_profile`, `app_config`).

3. **Each session gets isolated config**:
- Session A: `debug=true, user_api_key=xyz123`
- Session B: `debug=false, user_api_key=abc456`
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
# Start development server (with optional reload)
uv run dev                # Actually runs: uv run smithery dev
uv run dev --reload       # Auto-reload on code changes
uv run dev --log-level debug  # More verbose logging

# Start production server (optimized startup)
uv run start              # Actually runs: uv run smithery start
uv run start --log-level warning  # Minimal production logging
```

**Complete MCP Testing Workflow:**

1. Start server: `uv run dev` (runs on port 8081 by default)

2. **Test scenarios based on your config schema:**

   **Scenario A: Required fields (like `pirate_mode: bool = Field(...)`)** 
   ```bash
   # Must include required config - will get 422 error without it
   curl -X POST "http://127.0.0.1:8081/mcp?pirate_mode=true" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
   ```

   **Scenario B: Optional fields with defaults (like `debug: bool = Field(False)`)** 
   ```bash
   # Can omit config - will use defaults
   curl -X POST "http://127.0.0.1:8081/mcp" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
   ```

3. Get session ID from server logs: "Created new transport with session ID: [uuid]"

4. Send notifications/initialized with session header:
   ```bash
   curl -X POST "http://127.0.0.1:8081/mcp" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -H "mcp-session-id: [session-id]" \
     -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
   ```

5. Test your tools:
   ```bash
   curl -X POST "http://127.0.0.1:8081/mcp" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -H "mcp-session-id: [session-id]" \
     -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"hello","arguments":{"name":"World"}}}'
   ```

**Expected Responses:**
- With `pirate_mode=true`: `"Ahoy, World!"`
- With `pirate_mode=false` or default: `"Hello, World!"`
- Missing required fields: `422 error` with config schema


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
- **mcp>=1.6.0**: Model Context Protocol SDK
- **Python >=3.10**: Required Python version

### FastMCP Compatibility
The scaffold works with both:
- **MCP SDK FastMCP** (bundled with official mcp package)
- **FastMCP 2.0** (fastmcp package)

When using with existing FastMCP servers, ensure you have compatible versions:
- `mcp>=1.6.0` OR `fastmcp>=2.0.0`

### Security Considerations
- Session-scoped API keys and configuration
- CORS headers for web client compatibility
- Request logging and monitoring via gateway
- Authentication handled by Smithery platform

## Pre-Deployment Checklist

Before deploying, ensure your server works locally:

### 1. Basic Server Test
```bash
# Development server with timing info and reload support
uv run dev

# Production server with optimized startup (recommended for deployment testing)
uv run start
```

**What you'll see:**
- **Development mode**: `Server started in 45.2ms` (shows startup timing)
- **Production mode**: Minimal output, faster startup (no dev overhead)

**Common issues:**
- **"Module not found"**: Run `uv sync` first
- **"Server function not callable"**: Check your `[tool.smithery]` server reference in `pyproject.toml`
- **"Config schema errors"**: Verify your Pydantic model can be instantiated
- **Port unavailable**: In production mode, server fails fast instead of switching ports

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
- **Development**: `uv run dev --port 8000` (auto-switches if port busy)
- **Production**: `uv run start --port 8000` (fails fast if port unavailable)
- Kill existing process: `lsof -ti:8081 | xargs kill`

### Log Level Control
- **Development**: `uv run dev --log-level debug` (default: info)
- **Production**: `uv run start --log-level error` (default: warning)
- Available levels: critical, error, warning, info, debug, trace

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

## Community & Support

- **Discord**: Join our community for help and discussions: [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- **Bug Reports**: Found an issue? Report it on GitHub: [github.com/smithery-ai/sdk/issues](https://github.com/smithery-ai/sdk/issues)
- **Feature Requests**: Suggest new features on our GitHub discussions: [github.com/smithery-ai/sdk/discussions](https://github.com/smithery-ai/sdk/discussions)
