---
title: Smithery TypeScript MCP Server Scaffold
description: TypeScript MCP server template with tools, resources, prompts, and session configuration.
overview: Complete scaffold for building production-ready MCP servers. Run `npm run dev` to start or `npm run build` for production.
version: "1.0.0"
---

# AGENTS.md

Welcome to the **Smithery TypeScript MCP Server Scaffold**!

This is the template project that gets cloned when you run `npx create-smithery`. It provides everything you need to build, test, and deploy a Model Context Protocol (MCP) server with Smithery.

## Table of Contents

- [Project Structure](#project-structure)
- [Quick Start Commands](#quick-start-commands)
- [Core Components: Tools, Resources, and Prompts](#core-components-tools-resources-and-prompts)
- [Development Workflow](#development-workflow)
- [Deployment & CI/CD](#deployment--cicd)
- [Architecture Notes](#architecture-notes)
- [Pre-Deployment Checklist](#pre-deployment-checklist)

### Project Structure

```
your-server/
├── package.json           # Project dependencies and scripts
├── smithery.yaml          # Runtime specification (runtime: typescript)
├── src/
│   └── index.ts          # Main server implementation
└── README.md
```

## Quick Start Commands

```bash
# Run development server (streamable HTTP on port 8081)
# Opens interactive Smithery playground in your browser for testing
npm run dev          # or: bun run dev, pnpm run dev, yarn dev

# Build for production
npm run build        # or: bun run build, pnpm run build, yarn build
```

## Core Components: Tools, Resources, and Prompts

MCP servers expose three types of components that AI applications can interact with. Learn when to use each and how they work together to build powerful integrations.

### Tools: Executable Functions

Tools are executable functions that AI applications can invoke to perform actions:

```typescript
// Add a tool
server.registerTool(
  "hello",
  {
    title: "Hello Tool",
    description: "Say hello to someone",
    inputSchema: { name: z.string().describe("Name to greet") },
  },
  async ({ name }) => {
    return {
      content: [{ type: "text", text: `Hello, ${name}!` }],
    }
  },
)
```

### Resources: Read-Only Data Sources

Resources provide read-only data that gives AI applications context to work with. Unlike tools, resources do not perform actions—they simply return information:

```typescript
// Add a resource
server.registerResource(
  "hello-world-history",
  "history://hello-world",
  {
    title: "Hello World History",
    description: "The origin story of the famous 'Hello, World' program",
  },
  async uri => ({
    contents: [
      {
        uri: uri.href,
        text: '"Hello, World" first appeared in a 1972 Bell Labs memo by Brian Kernighan and later became the iconic first program for beginners in countless languages.',
        mimeType: "text/plain",
      },
    ],
  }),
)
```

### Prompts: Reusable Message Templates

Prompts are predefined message templates that help structure conversations. Use them to guide AI applications toward consistent interaction patterns:

```typescript
// Add a prompt
server.registerPrompt(
  "greet",
  {
    title: "Hello Prompt",
    description: "Say hello to someone",
    argsSchema: {
      name: z.string().describe("Name of the person to greet"),
    },
  },
  async ({ name }) => {
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Say hello to ${name}`,
          },
        },
      ],
    }
  },
)
```

### When to Use Each Component

**Use Tools when you need to:**
- Perform actions (create, update, delete operations)
- Execute computations or transformations
- Call external APIs
- Interact with databases or file systems

**Use Resources when you need to:**
- Provide reference data or documentation
- Share static or semi-static information
- Offer context without side effects
- Return data that AI applications can read

**Use Prompts when you need to:**
- Guide AI toward specific conversation patterns
- Reuse common interaction templates
- Structure multi-step workflows
- Maintain consistency across similar requests

### Session Configuration

Pass personalized settings to each connection—API keys, preferences, and user-specific configuration—without affecting other sessions.

**Why configuration matters:**
- **Multi-user support**: Different users have different API keys and settings
- **Security**: API keys stay session-scoped, not stored server-wide
- **Flexibility**: Users customize behavior at connection time without code changes

When you define a configuration schema using Zod, **Smithery automatically generates a configuration UI** and passes your settings as URL parameters. Each session gets isolated configuration—Session A and Session B don't interfere with each other.

#### How Smithery Uses Configuration

Smithery automatically:
- Generates a configuration form with appropriate input types
- Passes configurations as URL parameters to your server
- Shows helpful descriptions as form labels and tooltips
- Applies default values and enforces required fields

#### Real-World Example: Weather Server

Consider a weather server where different users need different settings. Users can customize their temperature unit, provide their API key, and set their default location:

```typescript
import { z } from "zod"

export const configSchema = z.object({
  weatherApiKey: z.string().describe("Your OpenWeatherMap API key"),
  temperatureUnit: z.enum(["celsius", "fahrenheit"]).default("celsius").describe("Temperature unit"),
  defaultLocation: z.string().default("New York").describe("Default city for weather queries"),
  debug: z.boolean().default(false).describe("Enable debug logging"),
})

export default function createServer({
  config,
}: {
  config: z.infer<typeof configSchema>
}) {
  // Your weather tools use config.weatherApiKey, config.temperatureUnit, etc.
}
```

**Usage scenarios:**
- **User A**: API key `abc123`, prefers Fahrenheit, lives in San Francisco
- **User B**: API key `xyz789`, prefers Celsius, lives in Singapore

Each user gets personalized weather data without affecting others.

#### Using Configuration in Your Server

The `config` object passed to your server function contains the session-specific settings. Here's how to access and use them:

```typescript
export default function createServer({
  config,
}: {
  config: z.infer<typeof configSchema>
}) {
  const server = new McpServer({
    name: "My Server",
    version: "1.0.0",
  })

  server.registerTool(
    "my-tool",
    {
      title: "My Tool",
      description: "Tool that uses session config",
      inputSchema: { name: z.string() },
    },
    async ({ name }) => {
      // Access session-specific config
      if (config.debug) {
        console.log(`DEBUG: Processing request for ${name}`)
      }
      
      // Use config values (API keys, preferences, etc.)
      const response = config.debug 
        ? `DEBUG: Hello ${name}`
        : `Hello ${name}`
      
      return {
        content: [{ type: "text", text: response }],
      }
    },
  )

  return server.server
}
```

#### How Session Config Works

1. **Define config schema**:
```typescript
export const configSchema = z.object({
  // Required field - users must provide this
  userApiKey: z.string().describe("Your API key"),
  
  // Optional fields with defaults - users can customize or use defaults
  debug: z.boolean().default(false).describe("Debug mode"),
  maxResults: z.number().default(10).describe("Maximum results to return"),
  
  // Optional field without default - can be undefined
  customEndpoint: z.string().optional().describe("Custom API endpoint"),
})
```

**Field Types:**
- **Required**: Use `z.string()`, `z.number()`, etc. - users must provide a value
- **Optional with default**: Use `.default(value)` - users can customize or use the default
- **Optional without default**: Use `.optional()` - completely optional

2. **Pass config via URL parameters** (the key-value pairs after the `?` in the URL):
```
http://localhost:3000/mcp?userApiKey=xyz123&debug=true
                          ↑ config passed as URL parameters
```

3. **Each session gets isolated config**:
- Session A: `debug=true, userApiKey=xyz123`
- Session B: `debug=false, userApiKey=abc456`
- Sessions don't interfere with each other

#### Configuration Management in Production

Once your server is published to Smithery, users can securely manage their configurations through a configuration UI. Saved configurations are automatically applied whenever they connect to your server in any client—no need to manually pass config parameters each time.

#### Stateful vs Stateless Servers

The TypeScript SDK provides two server patterns. **Choose stateless for most use cases.**

##### Stateless Servers (Recommended)

Stateless servers create a fresh instance for each request—no session state is maintained:

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { z } from 'zod'

// Optional: Define config schema
export const configSchema = z.object({
  apiKey: z.string().optional(),
  debug: z.boolean().default(false),
})

// Mark as stateless
export const stateless = true

// Your server creation function
export default function createServer({ config }: { config: z.infer<typeof configSchema> }) {
  const server = new McpServer({
    name: "My App",
    version: "1.0.0"
  })
  
  // Add tools, resources, prompts...
  
  return server.server
}
```

**Use stateless servers for:**
- API integrations
- Database queries
- File operations
- Most MCP servers

##### Stateful Servers (For Persistent State)

Stateful servers maintain state between calls within a session:

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { z } from 'zod'

// Optional: Define config schema
export const configSchema = z.object({
  apiKey: z.string().optional(),
  debug: z.boolean().default(false),
})

// Omit 'stateless' export or set to false for stateful behavior

// Your server creation function
export default function createServer({ 
  sessionId, 
  config 
}: { 
  sessionId: string
  config: z.infer<typeof configSchema> 
}) {
  const server = new McpServer({
    name: "My Stateful App",
    version: "1.0.0"
  })
  
  // You can store session-specific state here using sessionId
  // Example: const sessionState = getOrCreateState(sessionId)
  
  return server.server
}
```

**Use stateful servers for:**
- Chat conversations that need memory
- Multi-step workflows
- Game servers
- Any scenario requiring persistent state

## Development Workflow

This section covers how to customize the scaffold, test your server during development, and prepare for deployment.

### Customizing Your Project

**Customize the scaffold to match your actual project:**

1. **Update package.json:**
   ```json
   {
     "name": "your-project-name",
     "description": "Your MCP server description",
     "author": "Your Name"
   }
   ```

2. **Choose stateless or stateful (optional):**
   
   **Most servers should be stateless.** Only use stateful if you need to maintain state between requests (chat history, game state, etc.).
   
   For stateless (default, recommended):
   ```typescript
   export const stateless = true  // Optional: stateless is default behavior
   
   export default function createServer({ config }) {
     // Server created fresh for each request
   }
   ```
   
   For stateful:
   ```typescript
   // Omit 'stateless' export for stateful behavior
   
   export default function createServer({ sessionId, config }) {
     // sessionId lets you maintain state per session
   }
   ```

3. **Define your config schema (optional):**
   
   With config schema:
   ```typescript
   export const configSchema = z.object({
     apiKey: z.string().describe("Your API key"),
     debug: z.boolean().default(false).describe("Enable debug mode"),
   })
   
   export default function createServer({
     config,
   }: {
     config: z.infer<typeof configSchema>
   }) {
     const server = new McpServer({
       name: "Your Server Name",
       version: "1.0.0",
     })
     
     // Add your tools, resources, and prompts here
     
     return server.server
   }
   ```
   
   Without config schema:
   ```typescript
   export default function createServer() {
     const server = new McpServer({
       name: "Your Server Name",
       version: "1.0.0",
     })
     
     // Add your tools, resources, and prompts here
     
     return server.server
   }
   ```

### Testing Your Server: Three Approaches

Your MCP server can be tested in three different ways depending on your needs.

#### Smithery Playground

The fastest way to test your server during development:

```bash
npm run dev                # Actually runs: npx @smithery/cli dev
```

This starts your server locally on port 8081 with hot reload and opens an interactive Smithery playground in your browser. The playground lets you:
- Test your tools with a user-friendly UI
- Explore resources
- Try prompts
- Configure session settings in real-time
- View request/response details

**Best for:** Quick iteration, UI testing, tool validation

#### Custom Clients

Connect any MCP client to your server. Two options depending on your client type:

##### Option A: Local HTTP Clients

For command-line tools or local applications on the same machine:

1. Start the server: `npm run dev`
2. Connect to: `http://127.0.0.1:8081/mcp`
3. Include config parameters as URL query parameters:
```bash
http://127.0.0.1:8081/mcp?apiKey=your_key&debug=true
```

**Example with curl (simple test):**
```bash
curl -X POST "http://127.0.0.1:8081/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

##### Option B: Browser/Remote Clients (ngrok Tunnel)

For browser-based clients or testing from remote machines:

1. Start the server: `npm run dev`
2. Look for the ngrok tunnel URL in the console output (e.g., `https://abcd-1234-5678.ngrok.io`)
3. Connect your browser client to: `https://your-ngrok-id.ngrok.io/mcp`
4. Pass config as URL parameters:
```
https://your-ngrok-id.ngrok.io/mcp?apiKey=your_key&debug=true
```

**Best for:** Testing with remote clients, browser-based integrations, sharing with team members

#### Direct Protocol Testing

Test directly with curl commands for deep debugging or understanding the MCP protocol.

**Full MCP Testing Workflow:**

1. Start server:
```bash
npm run dev
```

2. Initialize connection (always include config params):
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

3. Get session ID from server response or logs (if using stateful server)

4. Send initialized notification:
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

5. Test tools:
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"hello","arguments":{"name":"World"}}}'
```

Expected response: `"Hello, World!"`

**Best for:** Protocol debugging, understanding MCP internals, automated testing scripts

## Deployment & CI/CD

Once you're ready to share your MCP server with the world, deploy it to Smithery:

1. **Publish your server**: Visit [smithery.ai/new](https://smithery.ai/new)
2. **Connect your repository**: Authorize Smithery to access your GitHub repository
3. **Automatic deployments**: By default, your server automatically deploys on every commit to the `main` branch
4. **Server scanning**: Smithery automatically discovers and indexes your tools, resources, and prompts

You can customize deployment settings (branch name, deployment triggers) in your Smithery dashboard after publishing.

## Troubleshooting

### Port Issues
- Default port is **8081**
- Kill existing process: `lsof -ti:8081 | xargs kill`

### Config Issues
```bash
# Check your configuration schema
node -e "import('./src/index.ts').then(m => console.log(JSON.stringify(m.configSchema._def, null, 2)))"
```

### Import Issues
- Ensure you're in the project root directory
- Run `npm install` to install dependencies
- Check that your TypeScript configuration is correct
- Verify Node.js version is 18 or higher

### TypeScript Issues
- Run `npx tsc --noEmit` to check for TypeScript errors
- Ensure all imports use `.js` extensions (TypeScript + ESM requirement)
- Check that your `package.json` has `"type": "module"`

## Resources

- **Documentation**: [smithery.ai/docs](https://smithery.ai/docs)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **TypeScript Quickstart**: [smithery.ai/docs/getting_started/quickstart_build_typescript.md](https://smithery.ai/docs/getting_started/quickstart_build_typescript.md)
- **GitHub**: [github.com/smithery-ai/sdk](https://github.com/smithery-ai/sdk)
- **Registry**: [smithery.ai](https://smithery.ai) for discovering and deploying MCP servers

## Community & Support

- **Discord**: Join our community for help and discussions: [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- **Bug Reports**: Found an issue? Report it on GitHub: [github.com/smithery-ai/sdk/issues](https://github.com/smithery-ai/sdk/issues)
- **Feature Requests**: Suggest new features on our GitHub discussions: [github.com/smithery-ai/sdk/discussions](https://github.com/smithery-ai/sdk/discussions)
