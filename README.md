# Smithery Typescript Framework [![npm version](https://badge.fury.io/js/@smithery%2Fsdk.svg)](https://badge.fury.io/js/@smithery%2Fsdk)

Smithery is a Typescript framework with utilities to make it easier to connect language models (LLMs) to [Model Context Protocols](https://modelcontextprotocol.io/) (MCPs), allowing you to build agents that use resources and tools without being overwhelmed by JSON schemas.

⚠️ _This repository is work in progress and in alpha. Not recommended for production use yet._ ⚠️

**Key Features**

- Connect to multiple MCPs with a single client
- Adapters to transform MCP responses for OpenAI and Anthropic clients
- Supports chaining tool calls until LLM completes

To find our registry of MCPs, visit [https://smithery.ai/](https://smithery.ai/).

# Quickstart

## Installation

```bash
npm install @smithery/sdk
```

## Usage

In this example, we'll connect to Exa search capabilities using either OpenAI or Anthropic.

```bash
npm install @smithery/sdk @modelcontextprotocol/sdk
```

The following code sets up the client and connects to an Exa MCP server:

```typescript
import { MultiClient } from "@smithery/sdk"
import { OpenAIChatAdapter } from "@smithery/sdk/integrations/llm/openai"
import { AnthropicChatAdapter } from "@smithery/sdk/integrations/llm/anthropic"
import { createTransport } from "@smithery/sdk/transport.js"
import { OpenAI } from "openai"
import Anthropic from "@anthropic-ai/sdk"

// Create a new connection
const exaTransport = createTransport(
  // Replace with your deployed MCP server URL
  "https://your-mcp-server.example.com"
)

// Initialize a multi-client connection
const client = new MultiClient()
await client.connectAll({
  exa: exaTransport,
  // You can add more connections here...
})

// Configure and authenticate
await client.clients.exa.request({
  method: "config",
  params: {
    config: {
      apiKey: process.env.EXA_API_KEY,
    },
  },
})
```

Now you can use either OpenAI or Anthropic to interact with the tools:

```typescript
// Using OpenAI
const openai = new OpenAI()
const openaiAdapter = new OpenAIChatAdapter(client)
const openaiResponse = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: "What AI events are happening in Singapore?" }],
  tools: await openaiAdapter.listTools(),
})
const openaiToolMessages = await openaiAdapter.callTool(openaiResponse)
```

For more complex interactions where the LLM needs to process tool outputs and potentially make additional calls, you'll need to implement a conversation loop. Here's an example:

```typescript
let messages = [
  {
    role: "user",
    content: "What are some AI events happening in Singapore and how many days until the next one?",
  },
]
const adapter = new OpenAIChatAdapter(client)
let isDone = false

while (!isDone) {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages,
    tools: await adapter.listTools(),
  })
  
  // Handle tool calls
  const toolMessages = await adapter.callTool(response)

  // Append new messages
  messages.push(response.choices[0].message)
  messages.push(...toolMessages)
  isDone = toolMessages.length === 0
}
```

See a full example in the [examples](./src/examples) directory.