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
- [smithery.yaml Configuration](#smitheryyaml-configuration)
- [Concepts](#concepts)
- [Development Workflow](#development-workflow)
- [Deployment & CI/CD](#deployment--cicd)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Community & Support](#community--support)

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

# Run on a custom port
npm run dev -- --port 3000

# Kill existing process if port 8081 is in use
lsof -ti:8081 | xargs kill

# Build for production
npm run build        # or: bun run build, pnpm run build, yarn build
```

## smithery.yaml Configuration

The `smithery.yaml` file configures how your server runs. For this TypeScript setup, it only needs:

### Required Field

```yaml
runtime: typescript
```

This tells Smithery to use the TypeScript runtime for your server.

### Optional Fields

#### target (optional)

Specifies where your server runs and determines the transport protocol. Can be `local` or `remote`:

```yaml
runtime: typescript
target: remote    # Options: remote (default) or local
```

- `local`: Server runs on the user's machine using stdio transport. When published, bundled into `.mcpb` file for distribution
- `remote`: Server runs on Smithery's infrastructure using HTTP transport (default)

See [Transports](#transports) for more details on how this affects your server's communication protocol.

#### env (optional)

Environment variables to inject when running your server. Available for both runtime types:

```yaml
runtime: typescript
env:
  NODE_ENV: "production"
  DEBUG: "true"
  LOG_LEVEL: "info"
```

## Concepts

### Core Components: Tools, Resources, and Prompts

MCP servers expose three types of components that AI applications can interact with. Learn when to use each and how they work together to build powerful integrations.

#### Tools: Executable Functions

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

#### Resources: Read-Only Data Sources

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

#### Prompts: Reusable Message Templates

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

#### When to Use Each Component

- **Tools**: Perform actions (create/update/delete, API calls, computations, database operations)
- **Resources**: Provide read-only data (documentation, reference info, context without side effects)
- **Prompts**: Guide conversation patterns (reusable templates, multi-step workflows, consistent interactions)

### Session Configuration

Pass personalized settings to each connection—API keys, preferences, and user-specific configuration—without affecting other sessions.

**Why configuration matters:**
- **Multi-user support**: Different users have different API keys and settings
- **Security**: API keys stay session-scoped, not stored server-wide
- **Flexibility**: Users customize behavior at connection time without code changes

When you define a configuration schema using Zod, Smithery automatically generates a configuration UI with appropriate input types, passes configurations as URL parameters to your server, and applies default values and enforces required fields. Each session gets isolated configuration—Session A and Session B don't interfere with each other.

#### How Session Config Works

1. **Define config schema** - Example weather server where different users have different settings:

```typescript
import { z } from "zod"

export const configSchema = z.object({
  // Required field - users must provide this
  weatherApiKey: z.string().describe("Your OpenWeatherMap API key"),
  // Optional fields with defaults - users can customize or use defaults
  temperatureUnit: z.enum(["celsius", "fahrenheit"]).default("celsius").describe("Temperature unit"),
  defaultLocation: z.string().default("New York").describe("Default city for weather queries"),
})
```

2. **Pass config via URL parameters**:
```
http://localhost:3000/mcp?weatherApiKey=abc123&temperatureUnit=fahrenheit
```

3. **Use config in your server**:
```typescript
export default function createServer({ config }: { config: z.infer<typeof configSchema> }) {
  const server = new McpServer({ name: "Weather Server", version: "1.0.0" })
  
  server.registerTool("get-weather", { /* ... */ }, async ({ city }) => {
    // Access session-specific config
    const temp = await fetchWeather(city, config.weatherApiKey)
    return formatTemp(temp, config.temperatureUnit)
  })
  
  return server.server
}
```

Each user gets personalized weather data without affecting others

#### Configuration Management in Production

Once your server is published to Smithery, users can securely manage their configurations through a configuration UI. Saved configurations are automatically applied whenever they connect to your server in any client—no need to manually pass config parameters each time.

### Transports

Transports define how your MCP server communicates with clients. The transport protocol is determined by the `target` field in your `smithery.yaml` file.

#### stdio Transport (Local Servers)

When `target: local`, your server uses **stdio transport**:

```yaml
runtime: typescript
target: local
```

**How it works:**
- Server communicates via standard input/output (stdin/stdout)
- Runs as a local process on the user's machine
- When published to Smithery, your server is bundled into a `.mcpb` file for distribution
- Users install and run it locally through their MCP client

**Best for:**
- File system access
- Local development tools
- Privacy-sensitive operations
- Servers that need direct access to user's machine

#### HTTP Transport (Remote Servers - Default)

When `target: remote` (or omitted, as remote is the default), your server uses **HTTP transport** and is hosted by Smithery:

```yaml
runtime: typescript
target: remote
```

**How it works:**
- Server communicates over HTTP/HTTPS
- Hosted on Smithery's infrastructure
- Accessible from anywhere via URL
- Smithery handles deployment, scaling, and availability

**Best for:**
- API integrations
- Cloud service wrappers
- Servers that don't need local file access
- Multi-user shared resources

**Note:** During development with `npm run dev`, all servers use HTTP transport (port 8081) regardless of the target setting. The target setting only affects production deployment.

### Stateful vs Stateless Servers

The TypeScript SDK provides two server patterns. **Servers are stateful by default.** Choose based on your needs.

#### Stateful Servers (Default)

Stateful servers maintain state between calls within a session:

```typescript
export default function createServer({ sessionId, config }) {
  const server = new McpServer({ name: "My Stateful App", version: "1.0.0" })
  
  console.log(`Session ${sessionId} started`)
  
  // Store session-specific state
  // Example: const sessionState = getOrCreateState(sessionId)
  
  return server.server
}
```

**Use stateful for:** Chat conversations, multi-step workflows, game servers, session analytics, or any scenario requiring persistent state.

#### Stateless Servers

Stateless servers create a fresh instance for each request—no session state is maintained:

```typescript
// Explicitly mark as stateless (opt-in behavior)
export const stateless = true

export default function createServer({ config }) {
  const server = new McpServer({ name: "My App", version: "1.0.0" })
  // Add tools, resources, prompts...
  return server.server
}
```

**Use stateless for:** Simple API integrations, one-off database queries, file operations, or servers that don't need session tracking.

## Development Workflow

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

2. **Choose stateless or stateful:** See [Stateful vs Stateless Servers](#stateful-vs-stateless-servers) for details. Servers are stateful by default. For stateless, export `export const stateless = true`.

3. **Define your config schema (optional):**
   
   ```typescript
   // With config schema
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
   
   // Without config schema: omit configSchema export and createServer takes no parameters
   ```

### Testing Your Server: Three Approaches

Your MCP server can be tested in three different ways depending on your needs. All approaches require running `npm run dev` first to start the server.

#### Smithery Playground

```bash
npm run dev                # Actually runs: npx @smithery/cli dev
```

Starts your server on port 8081 with hot reload and opens an interactive playground in your browser:
- Test your tools with a user-friendly UI
- Explore resources
- Try prompts
- Configure session settings in real-time
- View request/response details

**Best for:** Quick iteration, UI testing, tool validation

#### Custom Clients

Connect any MCP client to your server. Two options depending on your client type:

##### Option A: Local HTTP Clients

Connect to `http://127.0.0.1:8081/mcp` with config as URL parameters:
```
http://127.0.0.1:8081/mcp?apiKey=your_key&debug=true
```

##### Option B: Browser/Remote Clients (ngrok Tunnel)

1. Look for the ngrok tunnel URL in the console output (e.g., `https://abcd-1234-5678.ngrok.io`)
2. Connect your browser client to: `https://your-ngrok-id.ngrok.io/mcp`
3. Pass config as URL parameters:
```
https://your-ngrok-id.ngrok.io/mcp?apiKey=your_key&debug=true
```

**Best for:** Testing with remote clients, browser-based integrations, sharing with team members

#### Direct Protocol Testing

For deep debugging or understanding the MCP protocol:

1. Initialize connection (always include config params):
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

2. Send initialized notification:
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

3. List available tools:
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

4. Call a tool from the list (replace `tool-name` and arguments with your actual tool):
```bash
curl -X POST "http://127.0.0.1:8081/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"tool-name","arguments":{"key":"value"}}}'
```

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
