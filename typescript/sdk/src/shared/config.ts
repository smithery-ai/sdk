import type { Request as ExpressRequest } from "express"
import _ from "lodash"
import { err, ok } from "okay-error"
import type { z } from "zod"
import { zodToJsonSchema } from "zod-to-json-schema"

export interface SmitheryUrlOptions {
	// Smithery API key
	apiKey?: string
	// Configuration profile to use a config saved on Smithery
	profile?: string
	// Configuration object, which overrides the profile if provided
	config?: object
}

/**
 * Creates a URL to connect to the Smithery MCP server.
 * @param baseUrl The base URL of the Smithery server
 * @param options Optional configuration object
 * @returns A URL object with properly encoded parameters. Example: https://server.smithery.ai/{namespace}/mcp?config=BASE64_ENCODED_CONFIG&api_key=API_KEY
 */
export function createSmitheryUrl(
	baseUrl: string,
	options?: SmitheryUrlOptions,
) {
	const url = new URL(`${baseUrl}/mcp`)
	if (options?.config) {
		const param =
			typeof window !== "undefined"
				? btoa(JSON.stringify(options.config))
				: Buffer.from(JSON.stringify(options.config)).toString("base64")
		url.searchParams.set("config", param)
	}
	if (options?.apiKey) {
		url.searchParams.set("api_key", options.apiKey)
	}
	if (options?.profile) {
		url.searchParams.set("profile", options.profile)
	}
	return url
}

/**
 * Parses the config from an express request by checking the query parameter "config".
 * @param req The express request
 * @returns The config
 */
export function parseExpressRequestConfig(
	req: ExpressRequest,
): Record<string, unknown> {
	return JSON.parse(
		Buffer.from(req.query.config as string, "base64").toString(),
	)
}

/**
 * Parses and validates config from an Express request with optional Zod schema validation
 * Supports both base64-encoded config and dot-notation config parameters
 * @param req The express request
 * @param schema Optional Zod schema for validation
 * @returns Result with either parsed data or error response
 */
export function parseAndValidateConfig<T = Record<string, unknown>>(
	req: ExpressRequest,
	schema?: z.ZodSchema<T>,
) {
	// Parse config from request parameters
	let config: Record<string, unknown> = {}

	// 1. Process base64-encoded config parameter if present
	if (req.query.config) {
		try {
			config = parseExpressRequestConfig(req)
		} catch (configError) {
			return err({
				title: "Invalid config parameter",
				status: 400,
				detail: "Failed to parse config parameter",
				instance: req.originalUrl,
			})
		}
	}

	// 2. Process dot-notation config parameters (foo=bar, a.b=c)
	// This allows URL params like ?server.host=localhost&server.port=8080&debug=true
	for (const [key, value] of Object.entries(req.query)) {
		// Skip reserved parameters
		if (key === "config" || key === "api_key" || key === "profile") continue

		const pathParts = key.split(".")

		// Handle array values from Express query parsing
		const rawValue = Array.isArray(value) ? value[0] : value
		if (typeof rawValue !== "string") continue

		// Try to parse value as JSON (for booleans, numbers, objects)
		let parsedValue: unknown = rawValue
		try {
			parsedValue = JSON.parse(rawValue)
		} catch {
			// If parsing fails, use the raw string value
		}

		// Use lodash's set method to handle nested paths
		_.set(config, pathParts, parsedValue)
	}

	// Validate config against schema if provided
	if (schema) {
		const result = schema.safeParse(config)
		if (!result.success) {
			const jsonSchema = zodToJsonSchema(schema)

			const errors = result.error.issues.map(issue => {
				// Safely traverse the config object to get the received value
				let received: unknown = config
				for (const key of issue.path) {
					if (received && typeof received === "object" && key in received) {
						received = (received as Record<string, unknown>)[key]
					} else {
						received = undefined
						break
					}
				}

				return {
					param: issue.path.join(".") || "root",
					pointer: `/${issue.path.join("/")}`,
					reason: issue.message,
					received,
				}
			})

			return err({
				title: "Invalid configuration parameters",
				status: 422,
				detail: "One or more config parameters are invalid.",
				instance: req.originalUrl,
				configSchema: jsonSchema,
				errors,
			} as const)
		}
		return ok(result.data)
	}

	return ok(config as T)
}
