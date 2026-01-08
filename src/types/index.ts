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
}

export type StatefulServerContext<TConfig = unknown> = {
	config: TConfig
	session: Session
	env: Record<string, string | undefined>
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
}
