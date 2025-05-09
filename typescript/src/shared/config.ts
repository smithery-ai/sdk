import type express from "express"

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
	req: express.Request,
): Record<string, unknown> {
	return JSON.parse(
		Buffer.from(req.query.config as string, "base64").toString(),
	)
}
