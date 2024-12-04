import * as e2b from "@unroute/mcp-e2b"
import * as exa from "@unroute/mcp-exa"
import dotenv from "dotenv"
import EventSource from "eventsource"
import { OpenAI } from "openai"
import type { ChatCompletionMessageParam } from "openai/src/resources/index"
import { Connection } from "../src/index"
import { OpenAIHandler } from "../src/openai"

// Patch event source
// eslint-disable-next-line @typescript-eslint/no-explicit-any
global.EventSource = EventSource as any

async function main() {
	dotenv.config()
	// Initialize the OpenAI client
	const openai = new OpenAI()

	// Connect to MCPs
	const connection = await Connection.connect({
		exa: {
			server: exa.createServer(),
		},
		e2b: {
			server: e2b.createServer(),
		},
	})

	await connection.auth("exa", {
		apiKey: process.env.EXA_API_KEY,
	})
	await connection.auth("e2b", {
		apiKey: process.env.E2B_API_KEY,
	})

	// Example conversation with tool usage
	let isDone = false
	const messages: ChatCompletionMessageParam[] = [
		{
			role: "user",
			content:
				"Figure out the average of Biden and Trump's age in number of days. Figure out today's date as well.",
		},
	]

	const handler = new OpenAIHandler(connection)

	while (!isDone) {
		const response = await openai.chat.completions.create({
			model: "gpt-4o-mini",
			messages,
			tools: await handler.listTools(),
		})
		// Handle tool calls
		const toolMessages = await handler.call(response)

		messages.push(response.choices[0].message)
		messages.push(...toolMessages)
		isDone = toolMessages.length === 0
		console.log("messages", messages)
	}

	// Print the final conversation
	console.log("\nFinal conversation:")
	messages.forEach((msg) => {
		console.log(`\n${msg.role.toUpperCase()}:`)
		console.log(msg.content)
		if (msg.role === "assistant" && msg.tool_calls) {
			console.log(msg.tool_calls)
		}
	})
}

// Run the example
if (require.main === module) {
	main().catch((err) => {
		console.error("Error:", err)
		process.exit(1)
	})
}
