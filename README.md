# Unroute Typescript SDK

Unroute allows you to easily connect language models (LLMs) to [Model Context Protocols](https://modelcontextprotocol.io/) (MCPs), allowing it to use resources and tools/functions without setting up JSON schemas for each tool.

*This repository is work in progress.*

**Key Features**

- Connect to multiple MCPs with a single client
- Tool schema is handled automatically for the LLM
- Supports LLM reasoning through multiple tool calls

# Quickstart

## Installation

```bash
npm install @unroute/sdk
```

## Usage

In this example, we connect an LLM with the e2b code interpreter.

Unroute first requires you to create a connection to a set of MCPs. Each MCP is identified by a unique identifier (e.g. "e2b", "exa"), and has a set of environment variables (depending on the MCP).

```typescript
import unroute from "@unroute/sdk"
const connection = await unroute.connect({
  e2b: { 
    uri: "...",
    env: { E2B_API_KEY: "YOUR_API_KEY" }
  },
})
```

Now the connection is set up, you can wrap your LLM client around the connection.

```typescript
import unroute from "@unroute/sdk"
import { OpenAI } from "openai"

const connection = await unroute.connect({
  e2b: { 
    uri: "...",
    env: { E2B_API_KEY: "YOUR_API_KEY" }
  },
})
const client = connection.patch(new OpenAI())
const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: "What's 3+5?" }],
})
```

Your LLM will now be able to call the available tools in its completion and we'll automatically execute the tools before returning the response.

However, it's often the case where your LLM needs to call a tool, see its response, and continue processing output of the tool in order to give you a final response. In this case, you have to loop your LLM call and update your messages until the `isDone` property is set to `true`.

Here's a full example, which loops until the LLM has finished processing the tool response:

```typescript
import unroute from "@unroute/sdk"
import { OpenAI } from "openai"

const connection = await unroute.connect({
  e2b: { 
    uri: "...",
    env: { E2B_API_KEY: "YOUR_API_KEY" }
  },
})
const client = connection.patch(new OpenAI())

// Multi step tool execution
let isDone = false
let messages = [{ role: "user", content: "How old is Obama?" }]
while (!isDone) {
  const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages,
  })
  ;({ messages, isDone }) = connection.applyResponse(messages, response)
}
```

## Fine-grained control

You can opt-out of patching your LLM client, and instead use the following equivalent code:

```typescript
import unroute from "@unroute/sdk"
import { OpenAI } from "openai"

const connection = await unroute.connect({
  e2b: { 
    uri: "...",
    env: { E2B_API_KEY: "YOUR_API_KEY" }
  },
})
const client = new OpenAI()

// Multi step tool execution
let isDone = false
let messages = [{ role: "user", content: "How old is Obama?" }]
while (!isDone) {
  const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages,
    tools: await connection.getTools(),
  })
  const toolResponse = await connection.callTool(response)
  isDone = toolResponse.isDone
  ;({ messages, isDone }) = connection.applyResponse(messages, response)
}
```

# Troubleshooting
```
Error: ReferenceError: EventSource is not defined
```
This event means you're trying to use EventSource API (which is typically used in the browser) from Node. You'll have to install the following to use it:
```bash
npm install eventsource
npm install -D @types/eventsource
```

Patch the global EventSource object:
```typescript
import EventSource from "eventsource"
global.EventSource = EventSource as any