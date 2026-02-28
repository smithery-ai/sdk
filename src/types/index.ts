import type { Server } from "@modelcontextprotocol/sdk/server/index.js"
import type { Notification } from "@modelcontextprotocol/sdk/types.js"
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
		 * Send a notification directly to the connected client (via `transport.send()`),
		 * bypassing the server's notification handler chain.
		 * Use this for webhook → client notification routing.
		 */
		notify(sessionId: string, notification: Notification): Promise<void>
		/**
		 * Inject a raw JSON-RPC message into the server's handler chain for processing.
		 * The server's registered request/notification handlers will be invoked.
		 */
		dispatch(sessionId: string, message: unknown): Promise<void>
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
