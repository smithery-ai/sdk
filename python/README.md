# Smithery Python SDK

FastMCP servers with session-scoped configuration support.

## Installation

```bash
pip install smithery
```

## Usage

```python
from smithery import from_fastmcp
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

class ConfigSchema(BaseModel):
    debug: bool = False

server = from_fastmcp(FastMCP("My Server"), config_schema=ConfigSchema)

@server.tool()
def hello(name: str) -> str:
    ctx = server.get_context()
    config = ctx.session_config
    return f"Hello, {name}!" + (" (debug)" if config.get("debug") else "")

server.run(transport="streamable-http")
```

Configuration is passed via URL query parameters: `http://localhost:8000/mcp?debug=true`

See [scaffold](scaffold/) for a complete example with Docker support.