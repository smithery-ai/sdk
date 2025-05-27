# Smithery Typescript SDK

The SDK provides files for you to easily setup Smithery-compatible MCP servers and clients.

## Installation

```bash
npm install @smithery/sdk @modelcontextprotocol/sdk
```

## Usage

### Spawning a Server

Here's a minimal example of how to use the SDK to spawn an MCP server.

```typescript
import { createStatelessServer } from '@smithery/sdk/server/stateless.js'
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"

// Create your MCP server function
function createMcpServer({ config }) {
  // Create and return a server instance
  // https://github.com/modelcontextprotocol/typescript-sdk?tab=readme-ov-file#core-concepts
  const mcpServer = new McpServer({
    name: "My App",
    version: "1.0.0"
  })

  // ...
  
  return mcpServer.server
}

// Create the stateless server using your MCP server function.
createStatelessServer(createMcpServer)
  .app
  .listen(process.env.PORT || 3000)
```

This example:
1. Creates a stateless server that handles MCP requests
2. Defines a function to create MCP server instances for each session
3. Starts the Express server on the specified port. You must listen on the PORT env var if provided for the deployment to work on Smithery.

#### Stateful Server
Most API integrations are stateless.

However, if your MCP server needs to persist state between calls (i.e., remembering previous interactions in a single chat conversation), you can use the `createStatefulServer` function instead.