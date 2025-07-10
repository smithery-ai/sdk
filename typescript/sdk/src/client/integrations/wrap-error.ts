import type { Client } from "@modelcontextprotocol/sdk/client/index.js"
import type { RequestOptions } from "@modelcontextprotocol/sdk/shared/protocol.js"
import {
	type CallToolRequest,
	CallToolResultSchema,
	type CompatibilityCallToolResultSchema,
} from "@modelcontextprotocol/sdk/types.js"
import { patch } from "../../shared/patch.js"

/**
 * Wraps each tool call so any errors get sent back to the LLM instead of throwing
 */
export function wrapError<C extends Pick<Client, "callTool">>(client: C): C {
	patch(
		client,
		"callTool",
		callTool =>
			async (
				params: CallToolRequest["params"],
				resultSchema:
					| typeof CallToolResultSchema
					| typeof CompatibilityCallToolResultSchema = CallToolResultSchema,
				options?: RequestOptions,
			) => {
				try {
					return await callTool(params, resultSchema, options)
				} catch (err) {
					return {
						content: [
							{
								type: "text",
								text: JSON.stringify(err, Object.getOwnPropertyNames(err)),
							},
						],
						isError: true,
					}
				}
			},
	)

	return client
}
