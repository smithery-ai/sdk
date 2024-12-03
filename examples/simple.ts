import { OpenAI } from "openai"
import unroute from "../src/index"

import EventSource from "eventsource"
// Patch event source
// eslint-disable-next-line @typescript-eslint/no-explicit-any
global.EventSource = EventSource as any

async function main() {
  // Initialize the OpenAI client
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  })

  // Connect to MCPs
  const connection = await unroute.connect({
    e2b: {
      uri: process.env.E2B_URL || "https://sandbox.e2b.dev",
      env: { E2B_API_KEY: process.env.E2B_API_KEY! },
    },
  })

  // Patch the OpenAI client to use MCP tools
  const client = connection.patch(openai)

  // Example conversation with tool usage
  let isDone = false
  let messages = [
    {
      role: "user",
      content:
        "Write a python function that calculates the fibonacci sequence up to n numbers and run it for n=10",
    },
  ]

  while (!isDone) {
    const response = await client.chat.completions.create({
      model: "gpt-4",
      messages,
    })

    // Process the response and handle any tool calls
    const result = connection.applyResponse(messages, response)
    messages = result.messages
    isDone = result.isDone
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
