import { z } from "zod"

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
