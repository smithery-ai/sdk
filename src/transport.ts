import { WebSocketClientTransport } from "@modelcontextprotocol/sdk/client/websocket.js"

import { createSmitheryUrl } from "./config.js"

/**
 * Creates a transport to connect to the Smithery server
 * @param smitheryServerUrl The URL of the Smithery server (without trailing slash or protocol)
 * @param config Config to pass to the server
 * @returns Transport
 */
export function createTransport(smitheryServerUrl: string, config?: object) {
	let url: URL;
	try {
		// First try to parse as-is
		url = new URL(smitheryServerUrl);
		
		// For WebSocket connections, only ws: and wss: are valid
		if (url.protocol !== 'ws:' && url.protocol !== 'wss:') {
			// Special case: automatically convert http(s) to ws(s)
			if (url.protocol === 'http:' || url.protocol === 'https:') {
				console.warn(
					'Warning: HTTP/HTTPS protocol detected in smitheryServerUrl. ' +
					'Converting to WebSocket protocol. For better compatibility, ' +
					'consider providing the URL without a protocol.'
				);
				url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
			} else {
				throw new Error(
					`Protocol ${url.protocol} is not supported for WebSocket connections. ` +
					'Please use ws:// or wss:// (or provide URL without protocol)'
				);
			}
		}
	} catch (error) {
		// If initial parsing failed, try with default ws:// protocol
		try {
			url = new URL(`ws://${smitheryServerUrl}`);
		} catch {
			throw new Error(`Invalid URL provided: ${smitheryServerUrl}`);
		}
	}

	return new WebSocketClientTransport(
		createSmitheryUrl(`${url.toString()}/ws`, config),
	);
}
