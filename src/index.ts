import { Client } from "@modelcontextprotocol/sdk/client/index.js"
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js"
import {
	CallToolResultSchema,
	type Tool,
} from "@modelcontextprotocol/sdk/types.js"
import { v4 as uuidv4 } from "uuid"
import { z } from "zod"
import { ForwardTransport } from "./forward.js"
import {
	isServerConfig,
	isURIConfig,
	type MCPConfig,
	type Tools,
} from "./types.js"

export { AnthropicHandler } from "./anthropic.js"
export { OpenAIHandler } from "./openai.js"
export type { Tools, MCPConfig } from "./types.js"

export class Connection {
	mcps: Map<string, Client> = new Map()

	static async connect(config: MCPConfig) {
		const connection = new Connection()
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
					},
				)
				if (isURIConfig(mcpConfig)) {
					await mcp.connect(new SSEClientTransport(new URL(mcpConfig.url)))
				} else if (isServerConfig(mcpConfig)) {
					const server = mcpConfig.server
					const clientTransport = new ForwardTransport()
					const serverTransport = new ForwardTransport()
					clientTransport.bind(serverTransport)
					serverTransport.bind(clientTransport)

					await server.connect(serverTransport)
					await mcp.connect(clientTransport)
				}
				connection.mcps.set(mcpName, mcp)
			}),
		)
		return connection
	}

	async auth(mcpName: string, params: any) {
		await this.mcps.get(mcpName)?.request(
			{
				method: "auth",
				params,
			},
			z.object({}).passthrough(),
		)
	}

	// TODO: Invalidate cache on tool change
	private toolsCache: Tools | null = null

	async listTools(): Promise<Tools> {
		if (this.toolsCache === null) {
			this.toolsCache = (
				await Promise.all(
					Array.from(this.mcps.entries()).map(async ([name, mcp]) => {
						const capabilities = mcp.getServerCapabilities()
						if (!capabilities?.tools) return []
						const response = await mcp.listTools()
						return { [name]: response.tools } as Tool
					}),
				)
			).reduce((acc, curr) => Object.assign(acc, curr), {})
		}
		return this.toolsCache
	}

	async callTools(calls: { mcp: string; name: string; arguments: any }[]) {
		return await Promise.all(
			calls.map(async (call) => {
				const mcp = this.mcps.get(call.mcp)
				if (!mcp) {
					throw new Error(`MCP tool ${call.mcp} not found`)
				}
				return mcp.callTool(
					{
						name: call.name,
						arguments: call.arguments,
					},
					CallToolResultSchema,
				)
			}),
		)
	}
}
