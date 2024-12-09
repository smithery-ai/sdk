import type { Server } from "@modelcontextprotocol/sdk/server/index.js"

export type MCPConfig = Record<string, { server: Server } | { url: string }>

// Type guards
export function isServerConfig(
	config: { server: Server } | { url: string },
): config is { server: Server } {
	return "server" in config
}

export function isURIConfig(
	config: { server: Server } | { url: string },
): config is { url: string } {
	return "url" in config
}

import { z } from "zod"

export const ToolSchema = z.object({
	name: z.string(),
	description: z.string().optional(),
	inputSchema: z.record(z.unknown()),
})

export const ToolsSchema = z.record(z.array(ToolSchema))

export interface Tool extends z.infer<typeof ToolSchema> {}
export type Tools = z.infer<typeof ToolsSchema>
