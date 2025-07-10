import type {
	Message,
	MessageParam,
	Tool,
} from "@anthropic-ai/sdk/resources/index.js"

import type { Client } from "@modelcontextprotocol/sdk/client/index.js"
import type { RequestOptions } from "@modelcontextprotocol/sdk/shared/protocol.js"
import { CallToolResultSchema } from "@modelcontextprotocol/sdk/types.js"

/**
 * Adapt an MCP client so it works seamlessly with Anthropic messages
 */
export class AnthropicChatAdapter {
	constructor(private client: Pick<Client, "callTool" | "listTools">) {}

	async listTools(): Promise<Tool[]> {
		const toolResult = await this.client.listTools()
		return toolResult.tools.map(tool => ({
			name: tool.name,
			description: tool.description,
			input_schema: tool.inputSchema,
		}))
	}

	// TODO: Support streaming
	async callTool(
		response: Message,
		options?: RequestOptions,
	): Promise<MessageParam[]> {
		const content = response.content
		if (!content || content.length === 0) {
			return []
		}

		// Find tool calls in the message content
		const toolCalls = content.filter(part => part.type === "tool_use")

		if (toolCalls.length === 0) {
			return []
		}

		// Run parallel tool call
		const results = await Promise.all(
			toolCalls.map(async toolCall => {
				return await this.client.callTool(
					{
						name: toolCall.name,
						arguments: toolCall.input as any,
					},
					CallToolResultSchema,
					options,
				)
			}),
		)

		return [
			{
				role: "user",
				content: results.map((result, index) => ({
					tool_use_id: toolCalls[index].id,
					type: "tool_result" as const,
					// TODO: Find a way to remove the any
					content: (result.content as any).filter(
						(part: { type: string }) => part.type === "text",
					),
					is_error: Boolean(result.isError),
				})),
			},
		]
	}
}
