// src/registry.ts
import type { StdioServerParameters } from "@modelcontextprotocol/sdk/client/stdio.js"
import { REGISTRY_URL } from "./config.js"
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js"
import type { RegistryPackage, RegistryVariables } from "./types.js"
// import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js"

// Helper to create StdioClientTransport config
export function createStdioConfig(
  pkg: RegistryPackage, 
  variables: RegistryVariables
): StdioServerParameters {
  if (pkg.connections.length === 0) {
    throw new Error(`No connections defined for package: ${pkg.id}`)
  }

  // Use first connection for now - could add connection selection later
  const connection = pkg.connections[0]
  
  const env: Record<string, string> = {}
  if (connection.stdio.env) {
    for (const [key, template] of Object.entries(connection.stdio.env)) {
      env[key] = template.toString().replace(/\${([^}]+)}/g, (_: string, varName: string) => {
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
    env
  }
}

export async function fetchRegistryEntry(
  id: string,
): Promise<RegistryPackage | null> {
  try {
    const response = await fetch(`${REGISTRY_URL}/${id}`)
    if (!response.ok) {
      return null
    }
    return await response.json()
  } catch (error) {
    console.error("Error fetching registry entry:", error)
    return null
  }
}

export async function createTransport(
  id: string,
  variables: RegistryVariables
) {
  const pkg = await fetchRegistryEntry(id)
  if (!pkg) {
    throw new Error(`Registry package not found: ${id}`)
  }

  const config = createStdioConfig(pkg, variables)
  const transport = new StdioClientTransport(config)
  await transport.start()
  return transport
}

// Example usage:
/*
const transport = await createTransport("brave-search", {
  braveApiKey: "user-api-key"
})
*/
