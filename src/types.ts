import type { Server } from "@modelcontextprotocol/sdk/server/index"
import type { FunctionParameters } from "openai/resources"

export type MCPConfig = Record<string, { server: Server } | { url: string }>

// Type guards
export function isServerConfig(
  config: { server: Server } | { url: string }
): config is { server: Server } {
  return "server" in config
}

export function isURIConfig(
  config: { server: Server } | { url: string }
): config is { url: string } {
  return "uri" in config
}

export interface Tool {
  name: string
  description?: string
  inputSchema: FunctionParameters
}

export type Tools = { [mcp: string]: Tool[] }

export interface ListToolsResponse {
  _meta?: Record<string, any>
  nextCursor?: string
  tools: Tool[]
}
