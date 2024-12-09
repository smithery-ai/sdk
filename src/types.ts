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

export type URIConfig = { url: string } | { npm: string }

// Define a type for the internal wrapped server configuration
export type WrappedServerConfig = { server: Server }

// Update MCPConfig to accept both direct and wrapped server instances
export type MCPConfig = Record<string, Server | URIConfig | WrappedServerConfig>

// Type guards
export function isServerConfig(config: any): config is Server {
	return config instanceof Server
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

export function isWrappedServerConfig(config: any): config is WrappedServerConfig {
	return 'server' in config && config.server instanceof Server
}

export const ToolSchema = z.object({
	name: z.string(),
	description: z.string().optional(),
	inputSchema: z.record(z.unknown()),
})

export const ToolsSchema = z.record(z.array(ToolSchema))

export interface Tool extends z.infer<typeof ToolSchema> {}
export type Tools = z.infer<typeof ToolsSchema>
