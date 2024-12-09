import * as shellMcp from "@unroute/mcp-shell"
import dotenv from "dotenv"
import EventSource from "eventsource"
import { OpenAI } from "openai"
import type { ChatCompletionMessageParam } from "openai/resources/chat/index"
import { Connection } from "../src/index"
import { OpenAIHandler } from "../src/openai"
import url from 'url'
import readline from 'readline'

// Utility for human approval
async function getHumanApproval(command: string, args: string[]): Promise<boolean> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  })

  return new Promise((resolve) => {
    rl.question(
      `Command: ${command} ${args.join(' ')}\n` +  
      `Approve? [y/N]: `,
      (answer) => {
        rl.close()
        resolve(answer.toLowerCase() === 'y')
      }
    )
  })
}

// Patch event source
// eslint-disable-next-line @typescript-eslint/no-explicit-any
global.EventSource = EventSource as any

async function main() {
  dotenv.config()

  // Initialize the OpenAI client
  const openai = new OpenAI()

  // Connect to MCPs
  const connection = await Connection.connect({
    shell: {
      server: shellMcp.createServer({
        allowedCommands: ['ls', 'pwd', 'date', 'echo'],
        approvalHandler: getHumanApproval
      }),
    },
  })

  // Example conversation with tool usage
  let isDone = false
  const messages: ChatCompletionMessageParam[] = [
    {
      role: "user",
      content: "What's the date?",
    },
  ]

  const handler = new OpenAIHandler(connection)

  while (!isDone) {
    const response = await openai.chat.completions.create({
      model: "gpt-4-turbo-preview",
      messages,
      tools: await handler.listTools(),
    })

    // Handle tool calls - will prompt for approval during execution
    const toolMessages = await handler.call(response)
    messages.push(response.choices[0].message)
    messages.push(...toolMessages)
    isDone = toolMessages.length === 0
    console.log("Processing messages:", 
      messages.map(m => ({
        role: m.role,
        content: m.content,
        tools: ('tool_calls' in m) ? m.tool_calls?.length : 0
      }))
    )
  }

  // Print the final conversation
  console.log("\nFinal conversation:")
  messages.forEach((msg) => {
    console.log(`\n${msg.role.toUpperCase()}:`)
    console.log(msg.content)
    if (msg.role === "assistant" && msg.tool_calls) {
      console.log("Tool calls:", JSON.stringify(msg.tool_calls, null, 2))
    }
  })
}

// Run the example
if (import.meta.url === url.pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    console.error("Error:", err)
    process.exit(1)
  })
}