import { WebSocketClientTransport } from "@modelcontextprotocol/sdk/client/websocket.js"

import { createSmitheryUrl } from "./config.js"

/**
 * Creates a transport to connect to the Smithery server
 * @param smitheryServerUrl The URL of the Smithery server (without trailing slash or protocol)
 * @param config Config to pass to the server
 * @returns Transport
 */
export function createTransport(smitheryServerUrl: string, config?: object) {
	return new WebSocketClientTransport(
		createSmitheryUrl(`${smitheryServerUrl}/ws`, config),
	)
}
