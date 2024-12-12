// src/registry.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import type { StdioServerParameters } from "@modelcontextprotocol/sdk/client/stdio.js"
import { REGISTRY_URL } from "./config.js"

// Basic types for our registry
export interface RegistryEntry {
  id: string
  name: string
  description: string
  connection: {
    type: "stdio" | "sse" | "server"
    config: {
      command?: string
      args?: string[]
      envTemplate?: Record<string, string>
      url?: string
      server?: Server
    }
  }
}

// Helper to create StdioClientTransport config
export function createStdioConfig(
  entry: RegistryEntry, 
  variables: Record<string, string>
): StdioServerParameters {
  if (entry.connection.type !== "stdio") {
    throw new Error("Not a stdio connection")
  }

  const env: Record<string, string> = {}
  if (entry.connection.config.envTemplate) {
    const missingVars: string[] = []
    
    for (const [key, template] of Object.entries(entry.connection.config.envTemplate)) {
      env[key] = template.replace(/\${([^}]+)}/g, (_, varName) => {
        if (!(varName in variables)) {
          missingVars.push(varName)
          return ''
        }
        return variables[varName]
      })
    }

    if (missingVars.length > 0) {
      throw new Error(
        `Missing required environment variables: ${missingVars.join(', ')}`
      )
    }
  }

  return {
    command: entry.connection.config.command!,
    args: entry.connection.config.args,
    env
  }
}

export async function fetchRegistryEntry(
  id: string,
): Promise<RegistryEntry | null> {
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

// Example usage:
/*
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js"

const entry = await fetchRegistryEntry("brave-search")
if (entry) {
  const transportConfig = createStdioConfig(entry, {
    braveApiKey: "user-api-key"
  })
  const transport = new StdioClientTransport(transportConfig)
}
*/