import * as exa from "@unroute/mcp-exa"
import EventSource from "eventsource"
import { OpenAI } from "openai"
import { ChatCompletionMessageParam } from "openai/src/resources/index.js"
import { Connection } from "../src/index"
import { OpenAIHandler } from "../src/openai"

// Patch event source
// eslint-disable-next-line @typescript-eslint/no-explicit-any
global.EventSource = EventSource as any

async function main() {
  // Initialize the OpenAI client
  const openai = new OpenAI()

  // Connect to MCPs
  const connection = await Connection.connect({
    exa: {
      server: exa.createServer(),
    },
  })

  await connection.auth("exa", {
    apiKey: process.env.EXA_API_KEY,
  })

  // Example conversation with tool usage
  let isDone = false
  let messages: ChatCompletionMessageParam[] = [
    {
      role: "user",
      content:
        "Deduce Obama's age in number of days. It's November 28, 2024 today. Search to ensure correctness.",
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
  })
}

// Run the example
if (require.main === module) {
  main().catch((err) => {
    console.error("Error:", err)
    process.exit(1)
  })
}
