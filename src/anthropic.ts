import type { Message, MessageParam } from "@anthropic-ai/sdk/resources/index"

import type { Connection } from "./index.js"
import type { Tools } from "./types.js"

export class AnthropicHandler {
	constructor(private connection: Connection) {}

	async listTools(strict = false): Promise<any[]> {
		return this.format(await this.connection.listTools(), strict)
	}

	format(tools: Tools, strict = false): any[] {
		return Object.entries(tools).flatMap(([mcpName, tools]) =>
			tools.map((tool) => ({
				type: "function",
				function: {
					name: `${mcpName}_${tool.name}`,
					description: tool.description,
					parameters: tool.inputSchema,
					strict,
				},
			})),
		)
	}

	// TODO: Support streaming
	async call(response: Message): Promise<MessageParam[]> {
		const content = response.content
		if (!content || content.length === 0) {
			return []
		}

		// Find tool calls in the message content
		const toolCalls = content.filter((part) => part.type === "tool_use")

		if (toolCalls.length === 0) {
			return []
		}

		const results = await this.connection.callTools(
			toolCalls.map((toolCall) => {
				const splitPoint = toolCall.name.indexOf("_")
				const mcp = toolCall.name.slice(0, splitPoint)
				const name = toolCall.name.slice(splitPoint + 1)
				return {
					mcp,
					name,
					arguments: toolCall.input as object,
				}
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
