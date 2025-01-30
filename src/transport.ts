import { WebSocketClientTransport } from "@modelcontextprotocol/sdk/client/websocket.js"

import { createSmitheryUrl } from "./config.js"

/**
 * Creates a transport to connect to the Smithery server
 * @param smitheryServerUrl The URL of the Smithery server (without trailing slash or protocol)
 * @param config Config to pass to the server
 * @returns Transport
 */
export function createTransport(smitheryServerUrl: string, config?: object) {
	// Check if HTTP/HTTPS protocol was provided and warn user
	if (smitheryServerUrl.match(/^https?:\/\//)) {
		console.warn(
			'Warning: HTTP/HTTPS protocol detected in smitheryServerUrl. ' +
			'Converting to WebSocket protocol. For better compatibility, ' +
			'consider providing the URL without a protocol.'
		)
	}

	// First strip any existing protocol
	const cleanUrl = smitheryServerUrl.replace(/^(https?|wss?):\/\//, '')
	
	// Then add ws:// or wss:// based on whether the original was secure
	const wsUrl = smitheryServerUrl.startsWith('https') ? `wss://${cleanUrl}` : `ws://${cleanUrl}`
	
	return new WebSocketClientTransport(
		createSmitheryUrl(`${wsUrl}/ws`, config),
	)
}
