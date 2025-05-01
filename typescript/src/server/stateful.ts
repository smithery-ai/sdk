import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js"
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js"
import express from "express"
import { randomUUID } from "node:crypto"
import { parseExpressRequestConfig } from "../config.js"

import type { Server } from "@modelcontextprotocol/sdk/server/index.js"

/**
 * Arguments when we create a new instance of your server
 */
export interface CreateServerArg {
	sessionId: string
	config: Record<string, unknown>
}

export type CreateServerFn = (arg: CreateServerArg) => Server

/**
 * Creates a stateful server for handling MCP requests.
 * For every new session, we invoke createMcpServer to create a new instance of the server.
 * @param createMcpServer Function to create an MCP server
 * @returns Express app
 */
export function createStatefulServer(createMcpServer: CreateServerFn) {
	const app = express()
	app.use(express.json())

	// Map to store transports by session ID
	const transports: { [sessionId: string]: StreamableHTTPServerTransport } = {}

	// Handle POST requests for client-to-server communication
	app.post("/mcp", async (req, res) => {
		// Check for existing session ID
		const sessionId = req.headers["mcp-session-id"] as string | undefined
		let transport: StreamableHTTPServerTransport

		if (sessionId && transports[sessionId]) {
			// Reuse existing transport
			transport = transports[sessionId]
		} else if (!sessionId && isInitializeRequest(req.body)) {
			// New initialization request
			const newSessionId = randomUUID()
			transport = new StreamableHTTPServerTransport({
				sessionIdGenerator: () => newSessionId,
				onsessioninitialized: (sessionId) => {
					// Store the transport by session ID
					transports[sessionId] = transport
				},
			})

			// Clean up transport when closed
			transport.onclose = () => {
				if (transport.sessionId) {
					delete transports[transport.sessionId]
				}
			}

			try {
				const config = parseExpressRequestConfig(req)

				const server = createMcpServer({
					sessionId: newSessionId,
					config,
				})

				// Connect to the MCP server
				await server.connect(transport)
			} catch (error) {
				res.status(400).json({
					jsonrpc: "2.0",
					error: {
						code: -32000,
						message: "Bad Request: Invalid configuration",
					},
					id: null,
				})
				return
			}
		} else {
			// Invalid request
			res.status(400).json({
				jsonrpc: "2.0",
				error: {
					code: -32000,
					message: "Bad Request: No valid session ID provided",
				},
				id: null,
			})
			return
		}

		// Handle the request
		await transport.handleRequest(req, res, req.body)
	})

	// Reusable handler for GET and DELETE requests
	const handleSessionRequest = async (
		req: express.Request,
		res: express.Response,
	) => {
		const sessionId = req.headers["mcp-session-id"] as string | undefined
		if (!sessionId || !transports[sessionId]) {
			res.status(400).send("Invalid or missing session ID")
			return
		}

		const transport = transports[sessionId]

		await transport.handleRequest(req, res)
	}

	// Handle GET requests for server-to-client notifications via SSE
	app.get("/mcp", handleSessionRequest)

	// Handle DELETE requests for session termination
	app.delete("/mcp", handleSessionRequest)

	return { app }
}
