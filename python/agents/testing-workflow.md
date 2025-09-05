# MCP Server Testing Workflow

Complete testing workflow for Smithery-enhanced FastMCP servers with session-scoped configuration.

## Prerequisites

1. Server running on port (e.g., 8081)
2. Server enhanced with `@smithery.server()` decorator
3. Config schema defined (optional)

## Step-by-Step Testing Workflow

### Step 1: Initialize Session
Send POST request to `/mcp` with config parameters in URL query string:

```bash
curl -X POST "http://127.0.0.1:8081/mcp?access_token=test123&pirate_mode=false" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

**Expected Response:**
- HTTP 200 with initialization result
- Server logs: `Created new transport with session ID: [uuid]`

### Step 2: Send Initialized Notification
Use the session ID from server logs in header:

```bash
curl -X POST "http://127.0.0.1:8081/mcp?access_token=test123&pirate_mode=false" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: [session-id]" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

### Step 3: List Available Tools
```bash
curl -X POST "http://127.0.0.1:8081/mcp?access_token=test123&pirate_mode=false" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: [session-id]" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/list"}'
```

**Expected Response:**
- Tools listed with proper schema (no `ctx` parameter exposed)
- Only user parameters shown in `inputSchema`

### Step 4: Call Tools
```bash
curl -X POST "http://127.0.0.1:8081/mcp?access_token=test123&pirate_mode=false" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: [session-id]" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"hello","arguments":{"name":"World"}}}'
```

**Expected Response:**
- Tool executes successfully
- Returns result based on session config (e.g., "Hello, World!")

### Step 5: Test Different Configuration
Create new session with different config:

```bash
curl -X POST "http://127.0.0.1:8081/mcp?access_token=test123&pirate_mode=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

Get new session ID, then repeat steps 2-4 with the new session.

**Expected Response:**
- Different behavior based on config (e.g., "Ahoy, World!" with pirate_mode=true)

## Key Points

1. **Config in URL**: Always include config parameters in URL query string
2. **Session ID in Header**: Use `mcp-session-id` header for subsequent requests
3. **Config Persistence**: Each session maintains its own config throughout lifecycle
4. **Session Isolation**: Multiple sessions can have different configs simultaneously
5. **Tool Access**: Tools access config via `ctx.session_config` (not exposed in schema)

## Common Issues

- **Missing session ID**: Include `mcp-session-id` header in all requests after initialize
- **Missing config**: Always include config parameters in URL, even for subsequent requests
- **Wrong tool schema**: Ensure `ctx: Context` parameter is properly type-annotated
- **Config validation errors**: Check that all required config fields are provided

## Example Server Code

```python
from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field
from smithery.decorators import smithery

class ConfigSchema(BaseModel):
    access_token: str = Field(..., description="Your access token")
    pirate_mode: bool = Field(False, description="Speak like a pirate")

@smithery.server(config_schema=ConfigSchema)
def create_server():
    server = FastMCP("Say Hello")
    
    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """Say hello to someone."""
        session_config = ctx.session_config
        
        if not session_config.access_token:
            return "Error: Access token required"
            
        if session_config.pirate_mode:
            return f"Ahoy, {name}!"
        else:
            return f"Hello, {name}!"
    
    return server
```
