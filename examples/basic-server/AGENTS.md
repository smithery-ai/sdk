# AGENTS.md

Welcome to the **Smithery TypeScript MCP Server Scaffold**!

This is the template project that gets cloned when you run `npx create-smithery`. It provides everything you need to build, test, and deploy a Model Context Protocol (MCP) server with Smithery.

## What's Included

- **TypeScript MCP Server** with Zod-based configuration schema support
- **Example Tool** (`hello` tool with debug mode configuration)
- **Example Resource** (`history://hello-world` with Hello World origin story)
- **Example Prompt** (`greet` prompt for generating greeting messages)
- **Development Workflow** (`npm run dev` for local testing with hot reload)
- **Deployment Ready** configuration for the Smithery platform
- **Session Management** via `createStatefulServer` or `createStatelessServer` with optional config schemas

## Quick Start Commands

```bash
# Run development server (streamable HTTP on port 3000)
npm run dev

# Build for production
npm run build
```

## Development Workflow

Based on the [Model Context Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture.md), MCP servers provide three core primitives:

### 1. Tools (for actions)
Add executable functions that AI applications can invoke to perform actions:

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
    // Access session config if using stateful server
    const greeting = config.debug 
      ? `DEBUG: Hello, ${name}!`
      : `Hello, ${name}!`
    
    return {
      content: [{ type: "text", text: greeting }],
    }
  },
)
```

### 2. Resources (for static data) 
Add data sources that provide contextual information:

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

### 3. Prompts (for interaction templates)
Add reusable templates that help structure interactions:

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

### Project Structure

```
your-server/
├── package.json           # Project dependencies and scripts
├── smithery.yaml          # Runtime specification (runtime: typescript)
├── src/
│   └── index.ts          # Main server implementation
└── README.md
```

### Customizing Your Project

**Important:** You'll want to customize the scaffold to match your actual project:

1. **Update package.json:**
   ```json
   {
     "name": "your-project-name",
     "description": "Your MCP server description",
     "author": "Your Name"
   }
   ```

2. **Update your server function:**
   ```typescript
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

3. **Test your server works:**
   ```bash
   npm run dev
   ```

## Session Configuration

Session configuration allows clients to connect to your MCP server with personalized settings. Think of it like user preferences - each connection gets its own configuration that doesn't affect other sessions, perfect for passing API keys, customizing behavior, and personalizing responses.

When you define a configuration schema using Zod, Smithery automatically:
- **Generates a configuration UI** with form elements (text inputs, dropdowns, checkboxes)
- **Passes configurations to your server** as URL parameters  
- **Shows helpful descriptions** as form labels and tooltips
- **Applies default values** and enforces required fields

### Real-World Example: Weather Server

Let's say you're building a weather server. You might want users to customize their preferred temperature unit, provide an API key, or set their default location:

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

### Understanding Configuration

The `config` object is passed to your server creation function and contains session-specific configuration:

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

### How Session Config Works

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

2. **Pass config via URL parameters**:
```
http://localhost:3000/mcp?userApiKey=xyz123&debug=true
```

3. **Each session gets isolated config**:
- Session A: `debug=true, userApiKey=xyz123`
- Session B: `debug=false, userApiKey=abc456`
- Sessions don't interfere with each other

### Stateful vs Stateless Servers

The TypeScript SDK provides two server patterns:

#### Stateless Servers (Recommended for most use cases)
Each request creates a new server instance - no session state is maintained:

```typescript
import { createStatelessServer } from '@smithery/sdk/server/stateless.js'

// Your server creation function
function createMcpServer({ config }) {
  // Create and return a server instance
  const server = new McpServer({
    name: "My App",
    version: "1.0.0"
  })
  
  // Add tools, resources, prompts...
  
  return server.server
}

// Create the stateless server
createStatelessServer(createMcpServer, {
  schema: configSchema, // Optional Zod schema for config validation
})
  .app
  .listen(process.env.PORT || 3000)
```

**Use stateless servers for:**
- API integrations
- Database queries
- File operations
- Most MCP servers

#### Stateful Servers (For persistent state)
Maintains state between calls within a session:

```typescript
import { createStatefulServer } from '@smithery/sdk/server/stateful.js'

// Your server creation function
function createMcpServer({ sessionId, config }) {
  // sessionId allows you to maintain state per session
  const server = new McpServer({
    name: "My Stateful App",
    version: "1.0.0"
  })
  
  // You can store session-specific state here
  const sessionState = new Map()
  
  return server.server
}

// Create the stateful server
createStatefulServer(createMcpServer, {
  schema: configSchema, // Optional Zod schema for config validation
})
  .app
  .listen(process.env.PORT || 3000)
```

**Use stateful servers for:**
- Chat conversations that need memory
- Multi-step workflows
- Game servers
- Any scenario requiring persistent state

### Why This Matters

- **Multi-user support**: Different users can have different API keys/settings
- **Environment isolation**: Dev/staging/prod configs per session
- **Security**: API keys stay session-scoped, not server-global

### Secure Config Distribution (Production)

In production, Smithery handles sensitive configuration securely:

1. **Users save config in Smithery** (API keys, tokens, etc.)
2. **OAuth authentication** is built-in - no manual key management
3. **Smithery Gateway** securely forwards config to your server
4. **Your server receives config** via the `config` parameter as usual

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

#### Method 1: Smithery CLI Development Server
```bash
npm run dev                # Actually runs: npx @smithery/cli dev
```
This starts your server locally with hot reload. Perfect for development and testing changes quickly.

#### Method 2: Direct MCP Protocol Testing
```bash
# Start server
npm run dev               # Runs on port 3000 by default
```

**Complete MCP Testing Workflow:**
1. Start server: `npm run dev` (runs on port 3000 by default)
2. Initialize with config (always include config params): 
```bash
curl -X POST "http://127.0.0.1:3000/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```
3. Get session ID from server response or logs (if using stateful server)
4. Send notifications/initialized:
```bash
curl -X POST "http://127.0.0.1:3000/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```
5. Test the hello tool with debug mode:
```bash
curl -X POST "http://127.0.0.1:3000/mcp?debug=true" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"hello","arguments":{"name":"World"}}}'
```
Expected response: `"Hello, World!"` (with debug=false) or enhanced debug output (with debug=true)

### Deployment Configuration

**package.json:**
```json
{
  "scripts": {
    "dev": "npx @smithery/cli dev",
    "build": "npx @smithery/cli build"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.17.4",
    "zod": "^3.25.46"
  },
  "devDependencies": {
    "@smithery/cli": "^1.2.4"
  }
}
```

**smithery.yaml:**
```yaml
runtime: typescript
```

## Deployment & CI/CD

### Local Deployment
```bash
# TypeScript server deployment prep
npm run build             # Creates build artifacts
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
- **@modelcontextprotocol/sdk**: Official MCP TypeScript SDK
- **@smithery/cli**: Smithery CLI tools for development and deployment
- **zod**: Schema validation for configuration
- **Node.js >=18**: Required runtime version

### Security Considerations
- Session-scoped API keys and configuration
- CORS headers for web client compatibility
- Request logging and monitoring via gateway
- Authentication handled by Smithery platform

## Pre-Deployment Checklist

Before deploying, ensure your server works locally:

### 1. Basic Server Test
```bash
# This should start your server on localhost:3000
npm run dev
```

**Common issues:**
- **"Module not found"**: Run `npm install` first
- **"Server function not callable"**: Check your default export in `src/index.ts`
- **"Config schema errors"**: Verify your Zod schema can be instantiated

### 2. Validate Server Creation
```bash
# Test that your server function works
node -e "import('./src/index.ts').then(m => console.log(m.default({ config: {} })))"
```

**Expected output:** Should print something like `[object Object]` without errors. If you see import errors or exceptions, check your server configuration.

### 3. Test Configuration Schema
```bash
# Check that your config schema validates properly
node -e "import('./src/index.ts').then(m => console.log(m.configSchema.parse({ debug: true })))"
```

**Expected behavior:** Should parse and validate your config without errors.

## Troubleshooting

### Port Issues
- Default port is **3000**
- Change with: `PORT=8000 npm run dev`
- Kill existing process: `lsof -ti:3000 | xargs kill`

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
