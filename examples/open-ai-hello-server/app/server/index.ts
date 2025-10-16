import { createWidgetServer } from "@smithery/sdk/server"
import { widget } from "@smithery/sdk/helpers"
import { z } from "zod"
import type { GreeterState } from "./types.js"

export default function createServer() {
  // Create widget-enabled MCP server
  const server = createWidgetServer({
    name: "Hello Widget",
    version: "1.0.0",
  })

  // Register widget resource: auto-generates HTML from bundle
  const greeterResource = widget.resource({
    name: "greeter",
    description: "A simple greeting widget",
    bundle: ".smithery/greeter.js", // CLI builds this from app/web/src
    prefersBorder: true,
  })

  // Register tool: generates greeting and displays widget
  server.registerTool(
    "say-hello",
    {
      title: "Say Hello",
      description: "Greet someone by name",
      inputSchema: {
        name: z.string().min(1).describe("Name of person to greet"),
      }, // todo: this part could be more elegant
      _meta: {
        "openai/outputTemplate": greeterResource.uri,
        "openai/toolInvocation/invoking": "Preparing greeting...",
        "openai/toolInvocation/invoked": "Greeting ready!",
        "openai/widgetAccessible": true
      },
    },
    async (args) => {
      const { name } = args

      // Create greeting state
      const state: GreeterState = {
        name,
        greeting: `Hello, ${name}!`,
        timestamp: new Date().toISOString(),
      }

      // Return state to widget + message to model
      return widget.response({
        state,
        message: `Said hello to ${name}`,
      })
    }
  )

  server.registerResource(
    "greeter-widget",
    greeterResource.uri,
    greeterResource.metadata,
    greeterResource.handler
  )

  return server.server
}

