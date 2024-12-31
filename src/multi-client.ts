import { Client } from "@modelcontextprotocol/sdk/client/index.js"
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js"
import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import type { RequestOptions } from "@modelcontextprotocol/sdk/shared/protocol.js"
import type { Transport } from "@modelcontextprotocol/sdk/shared/transport.js"
import {
    type CallToolRequest,
    CallToolResultSchema,
    type CompatibilityCallToolResultSchema,
    type ListToolsRequest,
    type Tool,
} from "@modelcontextprotocol/sdk/types.js"

interface ClientInfo {
	name: string
	version: string
}
/**
 * A client that connects to multiple MCPs and provides a unified interface for
 * accessing their tools, treating them as a single MCP.
 */
export class MultiClient
	implements Pick<Client, "callTool" | "listTools" | "close">
{
	clients: Record<string, Client> = {}

	client_info: ClientInfo

	constructor(
		client_info?: ClientInfo,
		private client_capabilities: {
			capabilities: Record<string, unknown>
		} = {
			capabilities: {},
		},
	) {
		this.client_info = client_info || {
			name: "MultiClient",
			version: "1.0.0",
		}
	}

	/**
	 * Connects to a collection of transport or servers.
	 */
	async connectAll(transports: Record<string, Transport | Server>) {
		await Promise.all(
			Object.entries(transports).map(async ([namespace, transport]) => {
				const client = new Client(
					{
						name: this.client_info.name,
						version: "1.0.0",
					},
					this.client_capabilities,
				)

				if (transport instanceof Server) {
					const [clientTransport, serverTransport] =
						InMemoryTransport.createLinkedPair()

					await transport.connect(serverTransport)
					await client.connect(clientTransport)
				} else {
					await client.connect(transport)
				}
				this.clients[namespace] = client
			}),
		)
	}

	/**
	 * Maps a tool name to a namespace-specific name to avoid conflicts.
	 */
	toolNameMapper = (namespace: string, tool: Tool) => {
		return `${namespace}_${tool.name}`
	}
	toolNameUnmapper = (fullToolName: string) => {
		const namespace = fullToolName.split("_")[0]
		const toolName = fullToolName.split("_").slice(1).join("_")
		return { namespace, toolName }
	}

	/**
	 * List all tools available from all MCPs, ensuring each tool is namespaced.
	 * @param params - Optional parameters for the request.
	 * @param options - Optional options for the request.
	 * @returns A promise that resolves to an array of tools.
	 */
	async listTools(
		params?: ListToolsRequest["params"],
		options?: RequestOptions,
	) {
		const tools: Tool[] = (
			await Promise.all(
				Object.entries(this.clients).map(async ([namespace, mcp]) => {
					const capabilities = mcp.getServerCapabilities()
					if (!capabilities?.tools) return []
					const response = await mcp.listTools(params, options)
					return response.tools.map((tool) => ({
						...tool,
						name: this.toolNameMapper(namespace, tool),
					}))
				}),
			)
		).flat()
		return { tools }
	}

	async callTool(
		params: CallToolRequest["params"],
		resultSchema:
			| typeof CallToolResultSchema
			| typeof CompatibilityCallToolResultSchema = CallToolResultSchema,
		options?: RequestOptions,
	) {
		const { namespace, toolName } = this.toolNameUnmapper(params.name)

		const mcp = this.clients[namespace]
		if (!mcp) {
			throw new Error(`MCP tool ${namespace} not found`)
		}
		return mcp.callTool(
			{
				name: toolName,
				arguments: params.arguments,
			},
			resultSchema,
			options,
		)
	}

	async close() {
		await Promise.all(Object.values(this.clients).map((mcp) => mcp.close()))
	}
}
