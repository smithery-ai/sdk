import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"

export interface WidgetServerOptions {
  name: string
  version: string
}

export function createWidgetServer(options: WidgetServerOptions) {
  return new McpServer({
    name: options.name,
    version: options.version,
  })
}

