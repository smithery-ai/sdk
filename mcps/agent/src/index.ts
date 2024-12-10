import Anthropic from "@anthropic-ai/sdk"
import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
	RequestSchema,
	ResultSchema,
} from "@modelcontextprotocol/sdk/types.js"
import { z } from "zod"
import { zodToJsonSchema } from "zod-to-json-schema"
// TODO: use polyfill for client side?
import { humanId } from "human-id"
import { EventEmitter } from "node:events"

import type { PromptCachingBetaMessageParam } from "@anthropic-ai/sdk/resources/beta/prompt-caching/index.js"
import { AnthropicHandler } from "@smithery/sdk/integrations/llm/anthropic.js"
import { Connection, type MCPConfig } from "../../../dist/index.js"
// Define schemas for our tools
export const RunArgsSchema = z.object({
	instruction: z
		.string()
		.describe(
			"The instruction to execute. This is a prompt sent to a large language model. You will need to prompt in detail and ask specifically for a response from the model if needed.",
		),

	tools: z
		.array(z.string())
		.optional()
		.describe(
			"A subset of your tools (function names) that this agent can access. To avoid confusing the agent, only allow it to use the relevant tools. Defaults to enabling all tools.",
		),

	// TODO: fully implement timeout
	timeout: z
		.number()
		.int()
		.optional()
		.describe(
			"Maximum amount of time allocated to running the agent in seconds.",
		),
})

export const GetResultArgsSchema = z.object({
	pid: z
		.string()
		.describe("The process id of the process to get the result of."),
	block: z
		.number()
		.default(0)
		.describe(
			"Number of seconds to block and wait until the agent is finished running. 0 means no blocking.",
		),
})

export const ConfigSchema = z.object({
	apiKey: z.string().optional(),
	recursive: z.boolean().optional(),
	timeout: z
		.number()
		.int()
		.optional()
		.describe(
			"Default maximum amount of time allocated to running the agent in seconds.",
		),
	model: z
		.enum(["claude-3-5-sonnet-20241022"])
		.optional()
		.describe("The model to use. Default to 'claude-3-5-sonnet-20241022'."),
	maxTokens: z.number().optional(),
})

export const ConfigRequestSchema = RequestSchema.extend({
	method: z.literal("config"),
	params: ConfigSchema,
})
export const ConfigResultSchema = ResultSchema.extend({})

export type Config = z.infer<typeof ConfigSchema>

/**
 * Marks the last message with cache flag
 */
function cacheLastMessage(messages: PromptCachingBetaMessageParam[]) {
	const cachedMessages = JSON.parse(JSON.stringify(messages))
	const content = cachedMessages.at(-1)?.content
	if (Array.isArray(content)) {
		content[0].cache_control = { type: "ephemeral" }
	}
	return cachedMessages
}

export function createServer(
	mcpConfig: MCPConfig,
	config: Config = ConfigSchema.parse({}),
) {
	const server = new Server(
		{
			name: "mcp-agent",
			version: "1.0.0",
		},
		{
			capabilities: {
				tools: {},
			},
		},
	)

	// Initialize state
	const globals = {
		client: config.apiKey ? new Anthropic({ apiKey: config.apiKey }) : null,
	}
	interface Run {
		isRunning: boolean
		result: string | null
		agentEmitter: EventEmitter
	}
	// A set of processes
	const processes = new Map<string, Run>()

	server.setRequestHandler(ConfigRequestSchema, async (request) => {
		const { apiKey } = request.params
		globals.client = new Anthropic({ apiKey })
		Object.assign(config, ConfigSchema.parse(request.params))
		return {}
	})

	server.setRequestHandler(ListToolsRequestSchema, async () => {
		return {
			tools: [
				{
					name: "run",
					description:
						"Starts an autonomous agent that executes an instruction. This call will return immediately with no response and the agent will start running in the background. Think of this as an intern who can handle a subset of your tasks.",
					inputSchema: zodToJsonSchema(RunArgsSchema),
				},
				{
					name: "get_result",
					description:
						"Get the result of the agent. If the agent is not finished running and block time expired, this will return an error.",
					inputSchema: zodToJsonSchema(GetResultArgsSchema),
				},
			],
		}
	})

	server.setRequestHandler(CallToolRequestSchema, async (request) => {
		try {
			const { name, arguments: args } = request.params

			if (!globals.client) {
				throw new Error("Not authenticated.")
			}
			const client = globals.client

			switch (name) {
				case "run": {
					const parsed = RunArgsSchema.safeParse(args)
					if (!parsed.success) {
						throw new Error(`Invalid arguments: ${parsed.error}`)
					}
					// Start the execution asynchronously
					const procId = humanId()
					;(async () => {
						console.log(
							`[${procId}] Starting agent with parameters:`,
							JSON.stringify(parsed.data),
						)
						const run: Run = {
							isRunning: true,
							result: null,
							agentEmitter: new EventEmitter(),
						}
						processes.set(procId, run)

						const messages: PromptCachingBetaMessageParam[] = [
							{
								role: "user",
								content: parsed.data.instruction,
							},
						]

						let isDone = false

						// Connect to MCPs
						const connection = await Connection.connect(
							config.recursive
								? {
										agent: server,
										...mcpConfig,
									}
								: mcpConfig,
						)
						try {
							const handler = new AnthropicHandler(connection)
							while (!isDone) {
								let tools = await handler.listTools()
								// Filter tools
								if (parsed.data.tools) {
									tools = tools.filter((t) =>
										parsed.data.tools?.includes(t.name),
									)
								}
								const response =
									await client.beta.promptCaching.messages.create({
										model: config.model ?? "claude-3-5-sonnet-20241022",
										max_tokens: config.maxTokens ?? 1024,
										messages: cacheLastMessage(messages),
										tools,
									})
								// Handle tool calls
								const toolMessages = await handler.call(response)

								messages.push({
									role: "assistant",
									content: response.content,
								})
								messages.push(...toolMessages)
								isDone = toolMessages.length === 0

								console.log(
									`[${procId}] Assistant: `,
									response.content
										.map((c) =>
											c.type === "text"
												? c.text
												: `${c.name}: ${JSON.stringify(c.input)}`,
										)
										.join("\n"),
								)
								console.log(`[${procId}] Tools: `, JSON.stringify(toolMessages))
							}

							// Set the final result
							const lastContent = messages[messages.length - 1].content
							run.result =
								typeof lastContent === "string"
									? lastContent
									: JSON.stringify(lastContent)
						} catch (error) {
							run.result = `Error: ${error}`
						} finally {
							run.isRunning = false
							run.agentEmitter.emit("done")
							connection.close()
						}
					})()

					return {
						content: [
							{
								type: "text",
								text: JSON.stringify({
									status: "started",
									pid: procId,
								}),
							},
						],
					}
				}

				case "get_result": {
					const parsed = GetResultArgsSchema.safeParse(args)
					if (!parsed.success) {
						throw new Error(`Invalid arguments: ${parsed.error}`)
					}

					const run = processes.get(parsed.data.pid)
					if (!run) {
						throw new Error(`Process ${parsed.data.pid} not found.`)
					}

					if (run.isRunning) {
						// Wait until the agent is done
						await new Promise<void>((resolve) => {
							const timeout = setTimeout(() => {
								run.agentEmitter.removeListener("done", handleDone)
								resolve()
							}, parsed.data.block * 1000)
							const handleDone = () => {
								clearTimeout(timeout)
								resolve()
							}
							run.agentEmitter.once("done", handleDone)
						})
					}
					if (run.result === null) {
						throw new Error("Agent not started.")
					}

					// Delete run
					processes.delete(parsed.data.pid)

					return {
						content: [
							{
								type: "text",
								text: run.result,
							},
						],
					}
				}

				default:
					throw new Error(`Unknown tool: ${name}`)
			}
		} catch (error) {
			const errorMessage =
				error instanceof Error ? error.message : String(error)
			return {
				content: [
					{ type: "text", text: JSON.stringify({ error: errorMessage }) },
				],
				isError: true,
			}
		}
	})

	return server
}
