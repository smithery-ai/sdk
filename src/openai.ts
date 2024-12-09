import type { OpenAI } from "openai"
import type {
	ChatCompletionContentPartText,
	ChatCompletionTool,
	ChatCompletionToolMessageParam,
} from "openai/resources/index.js"

import type { RequestOptions } from "@modelcontextprotocol/sdk/shared/protocol.js"
import type { Connection } from "./index.js"
import type { Tools } from "./types.js"

export class OpenAIHandler {
	constructor(private connection: Connection) {}

	async listTools(strict = false): Promise<ChatCompletionTool[]> {
		return this.format(await this.connection.listTools(), strict)
	}

	format(tools: Tools, strict = false): ChatCompletionTool[] {
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
	async call(
		response: OpenAI.Chat.Completions.ChatCompletion,
		options?: RequestOptions,
	): Promise<ChatCompletionToolMessageParam[]> {
		const choice = response.choices[0]
		// TODO: Support `n`
		if (!choice) {
			return []
		}
		const toolCalls = choice.message?.tool_calls
		if (!toolCalls) {
			return []
		}

		const results = await this.connection.callTools(
			toolCalls.map((toolCall) => {
				const splitPoint = toolCall.function.name.indexOf("_")
				const mcp = toolCall.function.name.slice(0, splitPoint)
				const name = toolCall.function.name.slice(splitPoint + 1)
				return {
					mcp,
					name,
					arguments: JSON.parse(toolCall.function.arguments),
				}
			}),
			options,
		)
		return results.map((result, index) => ({
			role: "tool",
			content: result.content as ChatCompletionContentPartText[],
			tool_call_id: toolCalls[index].id,
		}))
	}
}
