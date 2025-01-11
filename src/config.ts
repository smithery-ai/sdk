import {
	ProgressTokenSchema,
	RequestSchema,
	ResultSchema,
} from "@modelcontextprotocol/sdk/types.js"
import { z } from "zod"

// Copied from MCP
export const BaseRequestSchema = z
	.object({
		_meta: z.optional(
			z
				.object({
					/**
					 * If specified, the caller is requesting out-of-band progress notifications for this request (as represented by notifications/progress). The value of this parameter is an opaque token that will be attached to any subsequent notifications. The receiver is not obligated to provide these notifications.
					 */
					progressToken: z.optional(ProgressTokenSchema),
				})
				.passthrough(),
		),
	})
	.passthrough()

/**
 * A custom method to set the configuration of the server deployed on Smithery.
 * This must be called after initialization and before using the SSE server.
 */
export const ConfigRequestSchema = RequestSchema.extend({
	method: z.literal("config"),
	params: BaseRequestSchema.extend({
		config: z.any(),
	}),
})

export type ConfigRequest = z.infer<typeof ConfigRequestSchema>

/**
 * A custom response schema to expected when creating a config request.
 */
export const ConfigResultSchema = ResultSchema.extend({
	error: z
		.any()
		.optional()
		.describe(
			"An object containing the error. If no error is present, it meanas the config succeeded.",
		),
}).describe("The result of a config request.")

export type ConfigResult = z.infer<typeof ConfigResultSchema>
