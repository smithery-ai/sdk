import type { Client } from "@modelcontextprotocol/sdk/client/index.js"
import { ToolListChangedNotificationSchema } from "@modelcontextprotocol/sdk/types.js"
import {
	// @ts-expect-error
	type inferParameters,
	jsonSchema,
	type Tool,
	tool,
	type ToolExecutionOptions,
} from "ai"
import type { JSONSchema7 } from "json-schema"

type ToolClient = Pick<
	Client,
	"listTools" | "callTool" | "setNotificationHandler"
>

/**
 * Watches the MCP client for tool changes and updates the tools object accordingly.
 * @param client The MCP client to watch
 * @returns A record of tool names to their implementations
 */
export async function watchTools(client: ToolClient) {
	const tools: Record<string, Tool> = {}

	client.setNotificationHandler(ToolListChangedNotificationSchema, async () => {
		Object.assign(tools, await listTools(client))
	})

	Object.assign(tools, await listTools(client))
	return tools
}

/**
 * Returns a set of wrapped AI SDK tools from the MCP server.
 * @returns A record of tool names to their implementations
 */
export async function listTools(client: ToolClient) {
	const tools: Record<string, Tool> = {}
	const listToolsResult = await client.listTools()
	for (const { name, description, inputSchema } of listToolsResult.tools) {
		const parameters = jsonSchema(inputSchema as JSONSchema7)

		tools[name] = tool({
			description,
			parameters,
			execute: async (
				args: inferParameters<typeof parameters>,
				options: ToolExecutionOptions,
			) => {
				options?.abortSignal?.throwIfAborted()
				const result = await client.callTool({
					name,
					arguments: args,
				})
				return result
			},
		})
	}
	return tools
}
