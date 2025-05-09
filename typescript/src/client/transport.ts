import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js"
import { createSmitheryUrl, type SmitheryUrlOptions } from "../shared/config.js"

/**
 * Creates a transport to connect to the Smithery server
 * @param baseUrl The URL of the Smithery server (without trailing slash or protocol)
 * @param options Optional configuration object
 * @returns Transport
 */
export function createTransport(baseUrl: string, options?: SmitheryUrlOptions) {
	return new StreamableHTTPClientTransport(createSmitheryUrl(baseUrl, options))
}
