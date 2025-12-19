import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js"
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js"
import type { AuthInfo } from "@modelcontextprotocol/sdk/server/auth/types.js"
import express from "express"
import { randomUUID } from "node:crypto"
import type { z } from "zod"
import { parseAndValidateConfig } from "../shared/config.js"

import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import * as zod from "zod"
import { type SessionStore, createLRUStore } from "./session.js"
import { createLogger } from "./logger.js"
import type { Logger } from "./logger.js"

/**
 * Arguments when we create a new instance of your server
 */
export interface CreateServerArg<T = Record<string, unknown>> {
	sessionId: string
	config: T
	auth?: AuthInfo
	logger: Logger
}

export type CreateServerFn<T = Record<string, unknown>> = (
	arg: CreateServerArg<T>,
) => McpServer["server"]

/**
 * Configuration options for the stateful server
 */
export interface StatefulServerOptions<T = Record<string, unknown>> {
	/**
	 * Session store to use for managing active sessions
	 */
	sessionStore?: SessionStore<StreamableHTTPServerTransport>
	/**
	 * Zod schema for config validation
	 */
	schema?: z.ZodSchema<T>
	/**
	 * Express app instance to use (optional)
	 */
	app?: express.Application
	/**
	 * Log level for the server (default: 'info')
	 */
	logLevel?: "debug" | "info" | "warn" | "error"
}

/**
 * Creates a stateful server for handling MCP requests.
 * For every new session, we invoke createMcpServer to create a new instance of the server.
 * @param createMcpServer Function to create an MCP server
 * @param options Configuration options including optional schema validation and Express app
 * @returns Express app
 */
export function createStatefulServer<T = Record<string, unknown>>(
	createMcpServer: CreateServerFn<T>,
	options?: StatefulServerOptions<T>,
) {
	const app = options?.app ?? express()

	app.use("/mcp", express.json())

	const sessionStore = options?.sessionStore ?? createLRUStore()

	const logger = createLogger(options?.logLevel ?? "info")

	// Handle POST requests for client-to-server communication
	app.post("/mcp", async (req, res) => {
		// Log incoming MCP request
		logger.debug(
			{
				method: req.body.method,
				id: req.body.id,
				sessionId: req.headers["mcp-session-id"],
			},
			"MCP Request",
		)

		// Check for existing session ID
		const sessionId = req.headers["mcp-session-id"] as string | undefined
		let transport: StreamableHTTPServerTransport

		if (sessionId && sessionStore.get(sessionId)) {
			// Reuse existing transport
			transport = sessionStore.get(sessionId)!
		} else if (!sessionId && isInitializeRequest(req.body)) {
			// New initialization request
			const newSessionId = randomUUID()
			transport = new StreamableHTTPServerTransport({
				sessionIdGenerator: () => newSessionId,
				onsessioninitialized: sessionId => {
					// Store the transport by session ID
					sessionStore.set(sessionId, transport)
				},
			})

			// Clean up transport when closed
			transport.onclose = () => {
				if (transport.sessionId) {
					sessionStore.delete?.(transport.sessionId)
				}
			}

			// New session - validate config
			const configResult = parseAndValidateConfig(req, options?.schema)
			if (!configResult.ok) {
				const status = (configResult.error.status as number) || 400
				logger.error(
					{ error: configResult.error, sessionId: newSessionId },
					"Config validation failed",
				)
				res.status(status).json(configResult.error)
				return
			}

			const config = configResult.value

			try {
				logger.info({ sessionId: newSessionId }, "Creating new session")
				const server = createMcpServer({
					sessionId: newSessionId,
					config: config as T,
					auth: (req as unknown as { auth?: AuthInfo }).auth,
					logger,
				})

				// Connect to the MCP server
				await server.connect(transport)
			} catch (error) {
				logger.error(
					{ error, sessionId: newSessionId },
					"Error initializing server",
				)
				res.status(500).json({
					jsonrpc: "2.0",
					error: {
						code: -32603,
						message: "Error initializing server.",
					},
					id: null,
				})
				return
			}
		} else {
			// Invalid request
			logger.warn({ sessionId }, "Session not found or expired")
			res.status(400).json({
				jsonrpc: "2.0",
				error: {
					code: -32000,
					message: "Session not found or expired",
				},
				id: null,
			})
			return
		}

		// Handle the request
		await transport.handleRequest(req, res, req.body)

		// Log successful response
		logger.debug(
			{
				method: req.body.method,
				id: req.body.id,
				sessionId: req.headers["mcp-session-id"],
			},
			"MCP Response sent",
		)
	})

	// Add .well-known/mcp-config endpoint for configuration discovery
	app.get("/.well-known/mcp-config", (req, res) => {
		// Set proper content type for JSON Schema
		res.set("Content-Type", "application/schema+json; charset=utf-8")

		// Create schema with metadata using Zod's native .meta()
		const schema = (options?.schema ?? zod.object({})).meta({
			title: "MCP Session Configuration",
			description: "Schema for the /mcp endpoint configuration",
			"x-query-style": "dot+bracket",
		})

		const configSchema = {
			...zod.toJSONSchema(schema, { target: "draft-2020-12" }),
			// $id is dynamic based on request, so we add it manually
			$id: `${req.protocol}://${req.get("host")}/.well-known/mcp-config`,
		}

		res.json(configSchema)
	})

	// Handle GET requests for server-to-client notifications via SSE
	app.get("/mcp", async (req: express.Request, res: express.Response) => {
		const sessionId = req.headers["mcp-session-id"] as string | undefined
		if (!sessionId || !sessionStore.get(sessionId)) {
			res.status(400).send("Invalid or expired session ID")
			return
		}

		const transport = sessionStore.get(sessionId)!

		await transport.handleRequest(req, res)
	})

	// Handle DELETE requests for session termination
	// https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#session-management
	app.delete("/mcp", async (req, res) => {
		const sessionId = req.headers["mcp-session-id"] as string | undefined

		if (!sessionId) {
			logger.warn("Session termination request missing session ID")
			res.status(400).json({
				jsonrpc: "2.0",
				error: {
					code: -32600,
					message: "Missing mcp-session-id header",
				},
				id: null,
			})
			return
		}

		const transport = sessionStore.get(sessionId)
		if (!transport) {
			logger.warn({ sessionId }, "Session termination failed - not found")
			res.status(404).json({
				jsonrpc: "2.0",
				error: {
					code: -32000,
					message: "Session not found or expired",
				},
				id: null,
			})
			return
		}

		// Close the transport
		transport.close?.()

		logger.info({ sessionId }, "Session terminated")

		// Acknowledge session termination with 204 No Content
		res.status(204).end()
	})

	return { app }
}
