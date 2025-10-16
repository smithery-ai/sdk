import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { widget } from "@smithery/sdk"
import type { GreeterState } from "./types.js"

export default function createServer() {
  const server = new McpServer({
    name: "Hello Widget",
    version: "1.0.0",
  })

  const greeterWidget = widget.resource({
    name: "greeter",
    description: "A simple greeting widget",
    bundle: ".smithery/greeter.js", // should be optional with default
  })

  server.registerTool(
    "say-hello",
    {
      title: "Say Hello",
      description: "Greet someone by name",
      inputSchema: {
        name: z.string().min(1).describe("Name of person to greet"),
      },
      _meta: greeterWidget.toolConfig({
        invoking: "Preparing greeting...",
        invoked: "Greeting ready!",
      }),
    },
    async (args) => {
      const { name } = args

      const state: GreeterState = {
        name,
        greeting: `Hello, ${name}!`,
        timestamp: new Date().toISOString(),
      }

      return widget.response({
        state,
        message: `Said hello to ${name}`,
      })
    }
  )

  server.registerResource(
    "greeter-widget",
    greeterWidget.uri,
    greeterWidget.metadata,
    greeterWidget.handler
  )

  return server.server
}

