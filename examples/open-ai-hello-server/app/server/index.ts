import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { widget } from "@smithery/sdk/openai"
import type { GreeterState } from "./types.js"

export default function createServer() {
  const server = new McpServer({
    name: "Hello Widget",
    version: "1.0.0",
  })

  // Using SDK helper to create widget resource
  // This automatically:
  // - Loads .smithery/greeter.js
  // - Constructs HTML with <div id="greeter-root">
  // - Sets uri to ui://widget/greeter.html
  // - Adds widget description to _meta
  const greeterWidget = widget.resource<GreeterState>({
    name: "greeter",
    description: "A simple greeting widget displaying personalized greetings",
  })

  // Register the resource using the SDK-generated handler
  server.registerResource(
    greeterWidget.name,
    greeterWidget.uri,
    {},
    greeterWidget.handler
  )

  server.registerTool(
    "say-hello",
    {
      title: "Say Hello",
      description: "Greet someone by name",
      inputSchema: {
        name: z.string().min(1).describe("Name of person to greet"),
      },
      // Using widget-specific toolConfig (knows template URI automatically)
      _meta: greeterWidget.toolConfig({
        invoking: "Preparing greeting...",
        invoked: "Greeting ready!",
      }),
    },
    async (args) => {
      const { name } = args

      const structuredData: GreeterState = {
        name,
        greeting: `Hello, ${name}!`,
        timestamp: new Date().toISOString(),
      }

      // Using widget-specific response helper (type-safe with GreeterState)
      return greeterWidget.response({
        structuredData,
        message: `Said hello to ${name}`,
      })
    }
  )

  return server.server
}

