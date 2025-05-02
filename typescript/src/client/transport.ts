import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js"
import { createSmitheryUrl } from "../config.js"

/**
 * Creates a transport to connect to the Smithery server
 * @param baseUrl The URL of the Smithery server (without trailing slash or protocol)
 * @param config Config to pass to the server
 * @param apiKey Optional API key for authentication
 * @returns Transport
 */
export function createTransport(
	baseUrl: string,
	config?: object,
	apiKey?: string,
) {
	return new StreamableHTTPClientTransport(
		createSmitheryUrl(`${baseUrl}`, config, apiKey),
	)
}
