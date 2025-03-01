import Anthropic from "@anthropic-ai/sdk"
import type { PromptCachingBetaMessageParam } from "@anthropic-ai/sdk/src/resources/beta/prompt-caching/index.js"
import dotenv from "dotenv"
import { exit } from "node:process"
import { OpenAI } from "openai"
import type { ChatCompletionMessageParam } from "openai/resources/index.mjs"
import { MultiClient } from "../index.js"
import { AnthropicChatAdapter } from "../integrations/llm/anthropic.js"
import { OpenAIChatAdapter } from "../integrations/llm/openai.js"
import { createTransport } from "../transport.js"

/**
 * Showcases a multi-tool calling example with OpenAI or Anthropic
 */
async function main() {
	dotenv.config()

	const args = process.argv.slice(2)
	const useOpenAI = args.includes("--openai")

	// Create a new connection
	const exaTransport = createTransport(
		// Note: this server may not exist. Replace with your deployment
		"https://exa-mcp-server-42082066756.us-central1.run.app",
		{
			apiKey: process.env.EXA_API_KEY,
		},
	)

	// Initialize a multi-client connection
	const client = new MultiClient()
	await client.connectAll({
		exa: exaTransport,
		// You can add more connections here...
	})

	// Example conversation with tool usage
	let isDone = false

	const chatState = useOpenAI
		? {
				type: "openai" as const,
				llm: new OpenAI(),
				messages: [] as ChatCompletionMessageParam[],
			}
		: {
				type: "anthropic" as const,
				llm: new Anthropic(),
				messages: [] as PromptCachingBetaMessageParam[],
			}

	chatState.messages.push({
		role: "user",
		content:
			"What are some AI events happening in Singapore and how many days until the next one?",
	})
	while (!isDone) {
		if (chatState.type === "openai") {
			const adapter = new OpenAIChatAdapter(client)
			const response = await chatState.llm.chat.completions.create({
				model: "gpt-4o-mini",
				messages: chatState.messages,
				tools: await adapter.listTools(),
			})
			chatState.messages.push(response.choices[0].message)
			const toolMessages = await adapter.callTool(response)
			chatState.messages.push(...toolMessages)
			isDone = toolMessages.length === 0
		} else {
			const adapter = new AnthropicChatAdapter(client)
			const response = await chatState.llm.beta.promptCaching.messages.create({
				model: "claude-3-5-sonnet-20241022",
				max_tokens: 256,
				messages: chatState.messages,
				tools: await adapter.listTools(),
			})
			chatState.messages.push({
				role: response.role,
				content: response.content,
			})
			const toolMessages = await adapter.callTool(response)
			chatState.messages.push(...toolMessages)
			isDone = toolMessages.length === 0
		}
		console.log("messages", JSON.stringify(chatState.messages, null, 2))
	}

	// Print the final conversation
	console.log("\nFinal conversation:")
	chatState.messages.forEach((msg) => {
		console.log(`\n${msg.role.toUpperCase()}:`)
		console.log(msg.content)
	})

	await client.close()
	exit(0)
}

// Run the example
main().catch((err) => {
	console.error("Error:", err)
	process.exit(1)
})
