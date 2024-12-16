// src/registry.ts
import type { StdioServerParameters } from "@modelcontextprotocol/sdk/client/stdio.js"
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js"
import { REGISTRY_URL } from "./config.js"
import {
	isStdio,
	type JSONSchema,
	type RegistryServer,
	type StdioConnection,
} from "./registry-types.js"

// Helper to create StdioClientTransport config
export function createStdioConfig(
	pkg: RegistryServer,
	variables: JSONSchema,
): StdioConnection {
	if (pkg.connections.length === 0) {
		throw new Error(`No connections defined for package: ${pkg.id}`)
	}

	// Use first connection for now - could add connection selection later
	const connection = pkg.connections[0]

	if (!isStdio(connection))
		throw new Error(`Connection not supported for stdio: ${connection}`)

	const env: Record<string, string> = {}
	if (connection.stdio.env) {
		for (const [key, template] of Object.entries(connection.stdio.env)) {
			env[key] = template
				.toString()
				.replace(/\${([^}]+)}/g, (_: string, varName: string) => {
					if (!(varName in variables)) {
						throw new Error(`Missing required variable: ${varName}`)
					}
					return variables[varName]
				})
		}
	}

	return {
		command: connection.stdio.command,
		args: connection.stdio.args,
		env: Object.keys(env).length > 0 ? env : undefined,
	}
}

export async function fetchRegistryEntry(id: string): Promise<RegistryServer> {
	const response = await fetch(`${REGISTRY_URL}/servers/${id}`)
	if (!response.ok) {
		throw new Error(`Registry entry not found: ${id}`)
	}
	return await response.json()
}

export async function createTransport(
	id: string,
	variables: JSONSchema = {},
	options: Partial<StdioServerParameters> = {},
) {
	const pkg = await fetchRegistryEntry(id)
	const config = createStdioConfig(pkg, variables)
	const transport = new StdioClientTransport({ ...config, ...options })
	return transport
}

// Example usage:
/*
const transport = await createTransport("brave-search", {
  braveApiKey: "user-api-key"
})
*/
