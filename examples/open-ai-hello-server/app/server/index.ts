import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { widget } from "@smithery/sdk"
import type { GreeterState } from "./types.js"

export default function createServer() {
  const server = new McpServer({
    name: "Hello Widget",
    version: "1.0.0",
  })

  const greeterWidget = widget.resource<GreeterState>({
    name: "greeter", // Used as resource ID, in URI (ui://widget/greeter.html), bundle path (.smithery/greeter.js), and HTML root ID
    description: "A simple greeting widget", // Becomes openai/widgetDescription in resource _meta
  })

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

      return greeterWidget.response({
        structuredData,
        message: `Said hello to ${name}`,
      })
    }
  )

  return server.server
}

