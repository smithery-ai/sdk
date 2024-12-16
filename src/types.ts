import { z } from "zod"

export const ToolSchema = z.object({
	name: z.string(),
	description: z.string().optional(),
	inputSchema: z.record(z.unknown()),
})

export const ToolsSchema = z.record(z.array(ToolSchema))

export interface Tool extends z.infer<typeof ToolSchema> {}
export type Tools = z.infer<typeof ToolsSchema>
