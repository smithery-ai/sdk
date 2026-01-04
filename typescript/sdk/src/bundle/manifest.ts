import { z } from "zod"

export const BundleManifestSchema = z.object({
	schemaVersion: z.literal("smithery.bundle.v1"),
	runtimeApiVersion: z.literal("smithery.isolate.v1"),
	entry: z.object({
		type: z.literal("esm"),
		export: z.string().default("default"),
	}),
	stateful: z.boolean().optional(),
	configSchema: z.record(z.string(), z.unknown()).optional(),
	capabilities: z
		.object({
			tools: z.array(z.record(z.string(), z.unknown())).optional(),
			resources: z.array(z.record(z.string(), z.unknown())).optional(),
			prompts: z.array(z.record(z.string(), z.unknown())).optional(),
		})
		.optional(),
	build: z
		.object({
			repo: z.string().optional(),
			commit: z.string().optional(),
			branch: z.string().optional(),
			builtAt: z.string().optional(),
		})
		.optional(),
})

export type BundleManifest = z.infer<typeof BundleManifestSchema>
