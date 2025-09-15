# Smithery Python SDK

Build FastMCP servers with Smithery integration - adds session-scoped configuration, and seamless deployment to the Smithery platform.

## Installation

```bash
# Recommended: using uv
uv add smithery

# Or using pip
pip install smithery
```

## Usage

```python
from smithery import Server
from pydantic import BaseModel

class ConfigSchema(BaseModel):
    debug: bool = False

@Server("My Server", config_schema=ConfigSchema)
def create_server():
    pass

@create_server.tool()
def hello(name: str) -> str:
    ctx = create_server.get_context()
    config = ctx.session_config
    # Access config using dot notation: config.debug
    return f"Hello, {name}!" + (" (debug)" if config.debug else "")

if __name__ == "__main__":
    create_server.run(transport="streamable-http")
```

# For servers without config schema, just use @Server("My Server")

Configuration is passed via URL query parameters: `http://localhost:8000/mcp?debug=true`

## CLI Commands

The SDK includes a CLI for development and testing:

```bash
# Initialize a new project
uvx smithery init

# Run server in development mode  
uv run smithery dev

# Run server with playground for testing
uv run smithery playground

# Run with specific transport and port
uv run smithery dev --transport shttp --port 8080 --reload
```

See [scaffold](scaffold/) for a complete example