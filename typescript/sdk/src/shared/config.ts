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

function isPlainObject(value: unknown): value is Record<string, unknown> {
	return value !== null && typeof value === "object" && !Array.isArray(value)
}

export function appendConfigAsDotParams(url: URL, config: unknown) {
	function add(pathParts: string[], value: unknown) {
		if (Array.isArray(value)) {
			for (let index = 0; index < value.length; index++) {
				add([...pathParts, String(index)], value[index])
			}
			return
		}
		if (isPlainObject(value)) {
			for (const [key, nested] of Object.entries(value)) {
				add([...pathParts, key], nested)
			}
			return
		}

		const key = pathParts.join(".")
		let stringValue: string
		switch (typeof value) {
			case "string":
				stringValue = value
				break
			case "number":
			case "boolean":
				stringValue = String(value)
				break
			default:
				stringValue = JSON.stringify(value)
		}
		url.searchParams.set(key, stringValue)
	}

	if (isPlainObject(config)) {
		for (const [key, value] of Object.entries(config)) {
			add([key], value)
		}
	}
}

/**
 * Creates a URL to connect to the Smithery MCP server.
 * @param baseUrl The base URL of the Smithery server
 * @param options Optional configuration object
 * @returns A URL with config encoded using dot-notation query params (e.g. model.name=gpt-4&debug=true)
 */
export function createSmitheryUrl(
	baseUrl: string,
	options?: SmitheryUrlOptions,
) {
	const url = new URL(`${baseUrl}/mcp`)
	if (options?.config) {
		appendConfigAsDotParams(url, options.config)
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
 * Parses and validates config from an Express request with optional Zod schema validation
 * Supports dot-notation config parameters (e.g., foo=bar, a.b=c)
 * @param req The express request
 * @param schema Optional Zod schema for validation
 * @returns Result with either parsed data or error response
 */
export function parseAndValidateConfig<T = Record<string, unknown>>(
	req: ExpressRequest,
	schema?: z.ZodSchema<T>,
) {
	const config = parseConfigFromQuery(Object.entries(req.query))

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

// Process dot-notation config parameters from query parameters (foo=bar, a.b=c)
// This allows URL params like ?server.host=localhost&server.port=8080&debug=true
export function parseConfigFromQuery(query: Iterable<[string, unknown]>) {
	const config: Record<string, unknown> = {}
	for (const [key, value] of query) {
		// Skip reserved parameters
		if (key === "api_key" || key === "profile") continue

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
	return config
}
