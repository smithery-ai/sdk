# Smithery SDK

TypeScript types for building MCP servers on the Smithery hosted runtime.

Docs: https://smithery.ai/docs/build

## Installation

```bash
npm install @smithery/sdk
```

## Usage

The SDK provides types for the Smithery runtime context that your MCP server receives when deployed.

```typescript
import type {
  ServerModule,
  ServerContext,
  Session,
} from "@smithery/sdk"
import { z } from "zod"

// Define your configuration schema
export const configSchema = z.object({
  apiKey: z.string(),
})

// Create your server
export default const createServer = async (context: ServerContext<z.infer<typeof configSchema>>) => {
  const { config, env } = context

  // Access user configuration
  console.log(config.apiKey)

  // Access environment variables
  console.log(env.MY_SECRET)

  // For stateful servers, access session storage
  if ("session" in context) {
    await context.session.set("key", "value")
    const value = await context.session.get("key")
  }

  // Return your MCP server instance
  return new Server({ name: "my-server", version: "1.0.0" }, { capabilities: {} })
}

```

## Types

### `ServerContext<TConfig>`

The context object passed to your server factory function:

- `config: TConfig` - User-provided configuration (validated against your `configSchema`)
- `env: Record<string, string | undefined>` - Environment variables
- `session?: Session` - Session storage (only for stateful servers)

### `Session`

Key-value storage scoped to the user session:

- `get<T>(key: string): Promise<T | undefined>`
- `set(key: string, value: unknown): Promise<void>`
- `delete(key: string): Promise<void>`

### `ServerModule<TConfig>`

The expected exports from your server entry point:

- `default: CreateServerFn<TConfig>` - Factory function that creates your MCP server
- `configSchema?: z.ZodSchema<TConfig>` - Zod schema for configuration validation
- `createSandboxServer?: CreateSandboxServerFn` - Optional function for deployment scanning
- `stateful?: boolean` - Whether the server maintains state between requests (default: `false`)

## Documentation

For complete documentation, see:
- [Quickstart Guide](https://smithery.ai/docs/build/quickstart)

## License

MIT
