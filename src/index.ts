import { OpenAI } from "openai"
import { ListToolsResponse, MCPConfig, UnrouteConnection } from "./types"
import { Client } from "@modelcontextprotocol/sdk/client/index.js"
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js"
import { v4 as uuidv4 } from "uuid"
import { Tool } from "@modelcontextprotocol/sdk/types"

class Unroute {
  private mcps: Map<string, Client>

  constructor() {
    this.mcps = new Map()
  }

  async connect(config: MCPConfig): Promise<UnrouteConnection> {
    // Initialize MCPs with their respective configs
    await Promise.all(
      Object.entries(config).map(async ([mcpName, mcpConfig]) => {
        const mcp = new Client(
          {
            name: uuidv4(),
            version: "1.0.0",
          },
          {
            capabilities: {},
          }
        )
        await mcp.connect(new SSEClientTransport(new URL(mcpConfig.uri)))
        this.mcps.set(mcpName, mcp)
      })
    )

    return {
      patch: this.patchOpenAI.bind(this),
      getTools: this.listTools.bind(this),
      callTool: this.callTool.bind(this),
      applyResponse: this.applyResponse.bind(this),
    }
  }

  private patchOpenAI(client: OpenAI): OpenAI {
    const originalCreate = client.chat.completions.create
    const getTools = this.listTools.bind(this)

    // @ts-ignore - We need to override the OpenAI client's create method
    client.chat.completions.create = async function (params: any) {
      const tools = await getTools()
      const response = originalCreate.call(this, { tools, ...params })
      return response
    }

    return client
  }

  private toolsCache: Tool[] | null = null

  private async listTools() {
    if (this.toolsCache === null) {
      this.toolsCache = (
        await Promise.all(
          Array.from(this.mcps.values()).map(async (mcp) => {
            const capabilities = mcp.getServerCapabilities()
            if (!capabilities?.tools) return []
            const response = await mcp.listTools()
            return response.tools
          })
        )
      ).flat()
    }
    return this.toolsCache
  }

  private async callTool(response: any) {
    const toolCalls = response.choices[0]?.message?.tool_calls
    if (!toolCalls) {
      return { isDone: true, messages: [] }
    }

    const results = await Promise.all(
      toolCalls.map(async (toolCall: any) => {
        const [mcpName, toolName] = toolCall.function.name.split(".")
        const mcp = this.mcps.get(mcpName)
        if (!mcp) {
          throw new Error(`MCP ${mcpName} not found`)
        }
        return mcp.callTool(toolName, JSON.parse(toolCall.function.arguments))
      })
    )

    const messages = results.map((result, index) => ({
      role: "tool",
      content: JSON.stringify(result),
      tool_call_id: toolCalls[index].id,
    }))

    return { isDone: false, messages }
  }

  private applyResponse(
    messages: Array<{ role: string; content: string }>,
    response: any
  ) {
    const newMessages = [...messages]
    const assistantMessage = response.choices[0].message
    newMessages.push(assistantMessage)

    const isDone = !assistantMessage.tool_calls
    return { messages: newMessages, isDone }
  }
}

export default new Unroute()
