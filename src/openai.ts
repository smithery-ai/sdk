import { OpenAI } from "openai"
import {
  ChatCompletionTool,
  ChatCompletionToolMessageParam,
} from "openai/resources"

import { Connection } from "."
import { Tools } from "./types"

export class OpenAIHandler {
  constructor(private connection: Connection) {}

  async listTools(strict: boolean = false): Promise<ChatCompletionTool[]> {
    return this.format(await this.connection.listTools(), strict)
  }

  format(tools: Tools, strict: boolean = false): ChatCompletionTool[] {
    return Object.entries(tools).flatMap(([mcpName, tools]) =>
      tools.map((tool) => ({
        type: "function",
        function: {
          name: `${mcpName}_${tool.name}`,
          description: tool.description,
          parameters: tool.inputSchema,
          strict,
        },
      }))
    )
  }

  // TODO: Support streaming
  async call(
    response: OpenAI.Chat.Completions.ChatCompletion
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
      toolCalls.map((toolCall) => ({
        mcp: toolCall.function.name.split("_")[0],
        name: toolCall.function.name.split("_")[1],
        arguments: JSON.parse(toolCall.function.arguments),
      }))
    )
    return results.map((result, index) => ({
      role: "tool",
      content: JSON.stringify(result),
      tool_call_id: toolCalls[index].id,
    }))
  }
}
