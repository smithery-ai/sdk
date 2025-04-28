/**
 * Creates a URL to connect to the Smithery MCP server
 * @param baseUrl The base URL of the Smithery server
 * @param config Optional configuration object
 * @param apiKey API key for authentication. Required if using Smithery.
 * @returns A URL object with properly encoded parameters
 */
export function createSmitheryUrl(
	baseUrl: string,
	config?: object,
	apiKey?: string,
) {
	const url = new URL(baseUrl)
	if (config) {
		const param =
			typeof window !== "undefined"
				? btoa(JSON.stringify(config))
				: Buffer.from(JSON.stringify(config)).toString("base64")
		url.searchParams.set("config", param)
	}
	if (apiKey) {
		url.searchParams.set("api_key", apiKey)
	}
	return url
}
