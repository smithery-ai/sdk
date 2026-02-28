import type { Server } from "@modelcontextprotocol/sdk/server/index.js"

import type { z } from "zod"

export type Session = {
	id: string
	get: <T = unknown>(key: string) => Promise<T | undefined>
	set: (key: string, value: unknown) => Promise<void>
	delete: (key: string) => Promise<void>
}

export type StatelessServerContext<TConfig = unknown> = {
	config: TConfig
	env: Record<string, string | undefined>
	accessToken?: string
}

export type StatefulServerContext<TConfig = unknown> = {
	config: TConfig
	session: Session
	env: Record<string, string | undefined>
	accessToken?: string
	/**
	 * Register a handler for messages sent via `sessions.send()`.
	 * This enables callback-based message passing outside the MCP protocol.
	 */
	onMessage: (handler: (message: unknown) => unknown | Promise<unknown>) => void
}

export type ServerContext<TConfig = unknown> =
	| StatelessServerContext<TConfig>
	| StatefulServerContext<TConfig>

export type SandboxServerContext = {
	session: Session
}

export type CreateServerFn<TConfig = unknown> = (
	context: ServerContext<TConfig>,
) => Server | Promise<Server>

export type CreateSandboxServerFn = (
	context: SandboxServerContext,
) => Server | Promise<Server>

/**
 * OAuth adapter for servers that require user authorization.
 * @unstable This interface is subject to change.
 */
export interface AuthAdapter {
	getAuthorizationUrl(args: {
		callbackUrl: string
		state: string
		codeChallenge?: string
		config: unknown
	}): Promise<{ authorizationUrl: string }>

	exchangeCode(args: {
		code: string
		callbackUrl: string
		codeVerifier?: string
		config: unknown
	}): Promise<{
		accessToken: string
		refreshToken?: string
		expiresIn?: number
	}>

	refreshToken(args: { refreshToken: string; config: unknown }): Promise<{
		accessToken: string
		refreshToken?: string
		expiresIn?: number
	}>
}

/**
 * Context passed to handleHttp for stateless servers.
 * @unstable This type is subject to change.
 */
export type StatelessHttpContext = {
	env: Record<string, string | undefined>
}

/**
 * Context passed to handleHttp for stateful servers.
 * @unstable This type is subject to change.
 */
export type StatefulHttpContext = {
	env: Record<string, string | undefined>
	sessions: {
		/**
		 * Send an arbitrary message to the session's registered `onMessage` handler.
		 * Returns the handler's response, or undefined if no handler is registered.
		 */
		send(sessionId: string, message: unknown): Promise<unknown>
	}
}

/**
 * Handler for non-MCP HTTP requests (e.g. webhook endpoints on subpaths).
 * @unstable This type is subject to change.
 */
export type HandleHttpFn = (
	request: Request,
	context: StatelessHttpContext | StatefulHttpContext,
) => Promise<Response>

/**
 * ServerModule - expected exports from an MCP server entry point
 */
export interface ServerModule<TConfig = unknown> {
	default: CreateServerFn<TConfig>
	configSchema?: z.ZodSchema<TConfig>
	createSandboxServer?: CreateSandboxServerFn
	/**
	 * Whether the server is stateful.
	 * Stateful servers maintain state between calls within a session.
	 * Stateless servers are fresh for each request.
	 * @default false
	 */
	stateful?: boolean
	createAuthAdapter?: (context: {
		env: Record<string, unknown>
	}) => Promise<AuthAdapter>
	handleHttp?: HandleHttpFn
}
