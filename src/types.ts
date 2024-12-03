import { OpenAI } from "openai"

export interface MCPConfig {
  [id: string]: {
    uri: string
    env: {
      [key: string]: string
    }
  }
}

export interface Tool {
  name: string
  description?: string
  inputSchema: {
    type: "object"
    properties?: Record<string, any>
  }
}

export interface ListToolsResponse {
  _meta?: Record<string, any>
  nextCursor?: string
  tools: Tool[]
}

export interface UnrouteConnection {
  patch: (client: OpenAI) => OpenAI
  getTools: () => Promise<any[]>
  callTool: (response: any) => Promise<{
    isDone: boolean
    messages: Array<{ role: string; content: string }>
  }>
  applyResponse: (
    messages: Array<{ role: string; content: string }>,
    response: any
  ) => {
    messages: Array<{ role: string; content: string }>
    isDone: boolean
  }
}
