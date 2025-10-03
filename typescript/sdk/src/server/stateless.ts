import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js"
import express from "express"
import type { z } from "zod"
import { parseAndValidateConfig } from "../shared/config.js"

import type { Server } from "@modelcontextprotocol/sdk/server/index.js"
import { zodToJsonSchema } from "zod-to-json-schema"
import type { AuthInfo } from "@modelcontextprotocol/sdk/server/auth/types.js"
import type { OAuthMountOptions } from "./auth/oauth.js"
import { type Logger, createLogger } from "./logger.js"

export type { Logger } from "./logger.js"

/**
 * Arguments when we create a stateless server instance
 */
export interface CreateStatelessServerArg<T = Record<string, unknown>> {
	config: T
	auth?: AuthInfo
	logger: Logger
}

export type CreateStatelessServerFn<T = Record<string, unknown>> = (
	arg: CreateStatelessServerArg<T>,
) => Server

/**
 * Configuration options for the stateless server
 */
export interface StatelessServerOptions<T = Record<string, unknown>> {
	/**
	 * Zod schema for config validation
	 */
	schema?: z.ZodSchema<T>
	/**
	 * Express app instance to use (optional)
	 */
	app?: express.Application
	oauth?: OAuthMountOptions
	/**
	 * Log level for the server (default: 'info')
	 */
	logLevel?: "debug" | "info" | "warn" | "error"
}

/**
 * Creates a stateless server for handling MCP requests.
 * Each request creates a new server instance - no session state is maintained.
 * This is ideal for stateless API integrations and serverless environments.
 *
 * @param createMcpServer Function to create an MCP server
 * @param options Configuration options including optional schema validation and Express app
 * @returns Express app
 */
export function createStatelessServer<T = Record<string, unknown>>(
	createMcpServer: CreateStatelessServerFn<T>,
	options?: StatelessServerOptions<T>,
) {
	const app = options?.app ?? express()

	const logger = createLogger(options?.logLevel ?? "info")

	app.use("/mcp", express.json())

	// Handle POST requests for client-to-server communication
	app.post("/mcp", async (req, res) => {
		// In stateless mode, create a new instance of transport and server for each request
		// to ensure complete isolation. A single instance would cause request ID collisions
		// when multiple clients connect concurrently.

		try {
			// Log incoming MCP request
			logger.debug(
				{
					method: req.body.method,
					id: req.body.id,
					params: req.body.params,
				},
				"MCP Request",
			)

			// Validate config for all requests in stateless mode
			const configResult = parseAndValidateConfig(req, options?.schema)
			if (!configResult.ok) {
				const status = (configResult.error.status as number) || 400
				logger.error({ error: configResult.error }, "Config validation failed")
				res.status(status).json(configResult.error)
				return
			}

			const config = configResult.value as T

			// Create a fresh server instance for each request
			const server = createMcpServer({
				config,
				auth: (req as unknown as { auth?: AuthInfo }).auth,
				logger,
			})

			// Create a new transport for this request (no session management)
			const transport = new StreamableHTTPServerTransport({
				sessionIdGenerator: undefined,
			})

			// Clean up resources when request closes
			res.on("close", () => {
				transport.close()
				server.close()
			})

			// Connect to the MCP server
			await server.connect(transport)

			// Handle the request directly
			await transport.handleRequest(req, res, req.body)

			// Log successful response
			logger.debug(
				{
					method: req.body.method,
					id: req.body.id,
				},
				"MCP Response sent",
			)
		} catch (error) {
			logger.error({ error }, "Error handling MCP request")
			if (!res.headersSent) {
				res.status(500).json({
					jsonrpc: "2.0",
					error: {
						code: -32603,
						message: "Internal server error",
					},
					id: null,
				})
			}
		}
	})

	// SSE notifications not supported in stateless mode
	app.get("/mcp", async (_req, res) => {
		res.status(405).json({
			jsonrpc: "2.0",
			error: {
				code: -32000,
				message: "Method not allowed.",
			},
			id: null,
		})
	})

	// Session termination not needed in stateless mode
	app.delete("/mcp", async (_req, res) => {
		res.status(405).json({
			jsonrpc: "2.0",
			error: {
				code: -32000,
				message: "Method not allowed.",
			},
			id: null,
		})
	})

	// Add .well-known/mcp-config endpoint for configuration discovery
	app.get("/.well-known/mcp-config", (req, res) => {
		// Set proper content type for JSON Schema
		res.set("Content-Type", "application/schema+json; charset=utf-8")

		const baseSchema = options?.schema
			? zodToJsonSchema(options.schema)
			: {
					type: "object",
					properties: {},
					required: [],
				}

		const configSchema = {
			$schema: "https://json-schema.org/draft/2020-12/schema",
			$id: `${req.protocol}://${req.get("host")}/.well-known/mcp-config`,
			title: "MCP Session Configuration",
			description: "Schema for the /mcp endpoint configuration",
			"x-query-style": "dot+bracket",
			...baseSchema,
		}

		res.json(configSchema)
	})

	return { app }
}
