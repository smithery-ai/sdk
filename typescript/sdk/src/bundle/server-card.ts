import {
    ImplementationSchema,
    PromptSchema,
    ResourceSchema,
    ToolSchema,
} from "@modelcontextprotocol/sdk/types.js"
import { z } from "zod"

export const ServerCardSchema = z
    .object({
        serverInfo: ImplementationSchema,
        authentication: z
            .object({
                required: z.boolean(),
                schemes: z.array(z.string()),
            })
            .optional(),
        tools: z.array(ToolSchema).optional(),
        resources: z.array(ResourceSchema).optional(),
        prompts: z.array(PromptSchema).optional(),
    })
    .passthrough()

export type ServerCard = z.infer<typeof ServerCardSchema>