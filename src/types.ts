import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import { z } from "zod"

export const MCPConfigSchema = z.record(
	z.string(),
	z.union([
		z.instanceof(Server),
		z.object({ server: z.instanceof(Server) }),
		z.object({ url: z.string() }),
		z.object({ pipe: z.string() }),
	]),
)

export type MCPConfig = z.infer<typeof MCPConfigSchema>

// Type guards
export function isServerConfig(config: any): config is Server {
	return config instanceof Server
}

export function isURIConfig(
	config: MCPConfig[string],
): config is { url: string } {
	return "url" in config && typeof config.url === "string"
}

export function isPipeConfig(
	config: MCPConfig[string],
): config is { pipe: string } {
	return "pipe" in config && typeof config.pipe === "string"
}

export function isWrappedServerConfig(
	config: any,
): config is { server: Server } {
	return "server" in config && config.server instanceof Server
}

export const ToolSchema = z.object({
	name: z.string(),
	description: z.string().optional(),
	inputSchema: z.record(z.unknown()),
})

export const ToolsSchema = z.record(z.array(ToolSchema))

export interface Tool extends z.infer<typeof ToolSchema> {}
export type Tools = z.infer<typeof ToolsSchema>
