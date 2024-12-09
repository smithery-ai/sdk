import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import { z } from "zod"

export const MCPConfigSchema = z.record(
	z.string(),
	z.union([
		z.object({ server: z.instanceof(Server) }),
		z.object({ url: z.string() }),
		z.object({ npm: z.string() }),
	]),
)

export type MCPConfig = z.infer<typeof MCPConfigSchema>

// Type guards
export function isServerConfig(
	config: MCPConfig[string],
): config is { server: Server } {
	return "server" in config && config.server instanceof Server
}

export function isURIConfig(
	config: MCPConfig[string],
): config is { url: string } {
	return "url" in config && typeof config.url === "string"
}

export function isNpmConfig(
	config: MCPConfig[string],
): config is { npm: string } {
	return "npm" in config && typeof config.npm === "string"
}

export const ToolSchema = z.object({
	name: z.string(),
	description: z.string().optional(),
	inputSchema: z.record(z.unknown()),
})

export const ToolsSchema = z.record(z.array(ToolSchema))

export interface Tool extends z.infer<typeof ToolSchema> {}
export type Tools = z.infer<typeof ToolsSchema>
