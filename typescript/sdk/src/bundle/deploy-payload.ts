import { z } from "zod"
import { ServerCardSchema } from "./server-card.js"

const HostedDeployPayloadSchema = z.object({
	type: z.literal("hosted"),
	stateful: z.boolean().default(false),
	configSchema: z.record(z.string(), z.unknown()).optional(),
	serverCard: ServerCardSchema.optional(),
	source: z
		.object({
			commit: z.string().optional(),
			branch: z.string().optional(),
		})
		.optional(),
})

const ExternalDeployPayloadSchema = z.object({
	type: z.literal("external"),
	upstreamUrl: z.string().url(),
})

export const DeployPayloadSchema = z.discriminatedUnion("type", [
	HostedDeployPayloadSchema,
	ExternalDeployPayloadSchema,
])

export type DeployPayload = z.infer<typeof DeployPayloadSchema>
