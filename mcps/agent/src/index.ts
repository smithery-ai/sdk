import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
	RequestSchema,
	ResultSchema,
	type ToolSchema,
} from "@modelcontextprotocol/sdk/types.js"
import Anthropic from "@anthropic-ai/sdk"
import { z } from "zod"
import { zodToJsonSchema } from "zod-to-json-schema"

// Define schemas for our tools
export const RunArgsSchema = z.object({
	instruction: z.string().describe("The instruction to execute. This is a prompt sent to a large language model. You will need to prompt in detail and ask specifically for a response from the model if needed."),
	model: z
		.enum(["claude-3-5-sonnet-20241022"])
		.default("claude-3-5-sonnet-20241022")
		.describe("The model to use. Default to 'claude-3-5-sonnet-20241022'."),
})

export const GetResultArgsSchema = z.object({
	block: z
		.number()
		.default(0)
		.describe(
			"Number of seconds to block and wait until the agent is finished running. 0 means no blocking.",
		),
})

type ToolInput = z.infer<typeof ToolSchema.shape.inputSchema>

// Auth schema for API key
export const AuthRequestSchema = RequestSchema.extend({
	method: z.literal("auth"),
	params: z.object({
		apiKey: z.string(),
	}),
})
export const AuthResultSchema = ResultSchema.extend({})

export function createServer() {
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
		client: null as Anthropic | null,
		isRunning: false,
		messages: [] as Array<any>,
		result: null as string | null,
	}

	server.setRequestHandler(AuthRequestSchema, async (request) => {
		const { apiKey } = request.params
		globals.client = new Anthropic({ apiKey })
		return {}
	})

	server.setRequestHandler(ListToolsRequestSchema, async () => {
		return {
			tools: [
				{
					name: "run",
					description:
						"Starts an autonomous agent that executes an instruction. This call will return immediately with no response and the agent will start running in the background. Think of this as an intern who can handle a subset of your tasks.",
					inputSchema: zodToJsonSchema(RunArgsSchema) as ToolInput,
				},
				{
					name: "get_result",
					description:
						"Get the result of the agent. If the agent is not finished running and block time expired, this will return an error.",
					inputSchema: zodToJsonSchema(GetResultArgsSchema) as ToolInput,
				},
			],
		}
	})

	server.setRequestHandler(CallToolRequestSchema, async (request) => {
		try {
			const { name, arguments: args } = request.params

			if (!globals.client) {
				throw new Error("Unrecoverable error: Not authenticated.")
			}
			const client = globals.client

			switch (name) {
				case "run": {
					const parsed = RunArgsSchema.safeParse(args)
					if (!parsed.success) {
						throw new Error(`Invalid arguments: ${parsed.error}`)
					}

					if (globals.isRunning) {
						throw new Error("Agent is already running an instruction")
					}

					globals.isRunning = true
					globals.result = null
					globals.messages = [
						{
							role: "user",
							content: parsed.data.instruction,
						},
					]

					// Start the execution asynchronously
					;(async () => {
						let isDone = false
						try {
							while (!isDone) {
								const response = await client.messages.create({
									model: parsed.data.model,
									max_tokens: 1024,
									messages: globals.messages,
								})

								globals.messages.push({
									role: "assistant",
									content: response.content,
								})

								// TODO: Support tool calling
								isDone = true
							}

							// Set the final result
							globals.result =
								globals.messages[globals.messages.length - 1].content
						} catch (error) {
							globals.result = `Error: ${error}`
						} finally {
							globals.isRunning = false
						}
					})()

					return {
						content: [
							{
								type: "text",
								text: "Started executing instruction",
							},
						],
					}
				}

				case "get_result": {
					const parsed = GetResultArgsSchema.safeParse(args)
					if (!parsed.success) {
						throw new Error(`Invalid arguments: ${parsed.error}`)
					}

					if (globals.isRunning) {
						// Wait until the agent is done
						while (globals.isRunning) {
							await new Promise((resolve) =>
								setTimeout(resolve, parsed.data.block * 1000),
							)
						}
					}

					if (globals.result === null) {
						throw new Error("No result available yet.")
					}

					return {
						content: [
							{
								type: "text",
								text: globals.result,
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
				content: [{ type: "text", text: `Error: ${errorMessage}` }],
				isError: true,
			}
		}
	})

	return server
}
