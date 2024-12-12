import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import { z } from "zod"

export const MCPConfigSchema = z.record(
	z.string(),
	z.union([
		z.instanceof(Server),
		z.object({ server: z.instanceof(Server) }),
		z.object({ url: z.string() }),
		z.object({
			stdio: z.object({
				command: z
					.string()
					.describe("The executable to run to start the server."),
				args: z
					.array(z.string())
					.optional()
					.describe("Command line arguments to pass to the executable."),
				env: z
					.record(z.string(), z.string())
					.optional()
					.describe(
						"The environment to use when spawning the process. If not specified, the result of getDefaultEnvironment() will be used.",
					),
			}),
		}),
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

export function isStdioConfig(config: MCPConfig[string]): config is {
	stdio: { command: string; args?: string[]; env?: Record<string, string> }
} {
	return "stdio" in config
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

// Registry types
type StdioConfig = { 
	command: string
	args: string[]
	env?: Record<string, string>
}

export interface RegistryPackage {
	id: string
	name: string
	description: string
	vendor: string
	sourceUrl: string
	license: string
	homepage: string
	connections: Array<{
		configSchema: Record<string, any>
		stdio: StdioConfig
	}>
}

export type RegistryVariables = Record<string, string>


