/**
 * Types for entries in the Smithery registry
 */
import { z } from "zod"

export const JSONSchemaSchema: z.ZodType = z
	.lazy(() =>
		z.object({
			type: z.string().optional(),
			properties: z.record(JSONSchemaSchema).optional(),
			items: JSONSchemaSchema.optional(),
			required: z.array(z.string()).optional(),
			description: z.string().optional(),
			default: z.unknown().optional(),
		}),
	)
	.describe(
		"JSON Schema defines the configuration required to initialize the server. All variables are used to template fill the commands. Leave undefined if no config required.",
	)

export type JSONSchema = z.infer<typeof JSONSchemaSchema>

export const StdioConnectionSchema = z.object({
	command: z.string().describe("The executable to run to start the server."),
	args: z
		.array(z.string())
		.optional()
		.describe("Command line arguments to pass to the executable."),
	env: z
		.record(z.string(), z.string())
		.optional()
		.describe("The environment to use when spawning the process."),
})

export type StdioConnection = z.infer<typeof StdioConnectionSchema>

export const ConnectionSchema = z
	.object({
		configSchema: JSONSchemaSchema.optional(),
	})
	.and(
		z.union([
			z.object({
				sse: z.string().describe("The URL to connect to the server."),
			}),
			z.object({
				stdio: StdioConnectionSchema,
			}),
		]),
	)
	.describe(
		"A connection represents the protocol used to connect with the MCP server. A connection can be templated with shell variables in the format of ${VARNAME}. These will be replaced with the actual value of the variable defined in `configSchema` in durnig runtime.",
	)

export type Connection = z.infer<typeof ConnectionSchema>

export const RegistryServerSchema = z.object({
	id: z
		.string()
		.describe("The unique identifier. Usually the `npm` package name."),
	name: z.string().describe("The human-readable name of the MCP server."),
	verified: z
		.boolean()
		.optional()
		.describe(
			"Whether the server is maintained by the official API maintainers.",
		),
	description: z
		.string()
		.optional()
		.describe("A concise description of the MCP server for end-users."),
	vendor: z.string().describe("The name of the author of the MCP."),
	sourceUrl: z
		.string()
		.describe("A URL to the official page of the MCP repository."),
	license: z.string().optional().describe("The license of the MCP."),
	homepage: z
		.string()
		.describe(
			"The URL to the homepage of the MCP, typically the product page.",
		),
	connections: z
		.array(ConnectionSchema)
		.describe("A list of ways to connect with the MCP server."),
})

export type RegistryServer = z.infer<typeof RegistryServerSchema>

// Type guard
export function isStdio(
	connection: Connection,
): connection is Connection & { stdio: StdioConnection } {
	return "stdio" in connection
}
