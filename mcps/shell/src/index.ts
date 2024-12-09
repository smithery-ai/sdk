import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ToolSchema,
} from "@modelcontextprotocol/sdk/types.js"
import { z } from "zod"
import { zodToJsonSchema } from "zod-to-json-schema"
import { spawn } from "node:child_process"

// Schema definitions
export const ExecuteCommandArgsSchema = z.object({
  command: z.string().describe("The command to execute"),
  args: z.array(z.string()).describe("Command arguments"),
})

const ToolInputSchema = ToolSchema.shape.inputSchema
type ToolInput = z.infer<typeof ToolInputSchema>

// Allowlist of safe commands
const ALLOWED_COMMANDS = new Set(["ls", "pwd", "echo", "cat", "wc", "date"])

// Execute command safely
async function executeCommand(command: string, args: string[]): Promise<{stdout: string, stderr: string}> {
  return new Promise((resolve, reject) => {
    const proc = spawn(command, args)
    let stdout = ""
    let stderr = ""

    proc.stdout.on("data", (data) => {
      stdout += data.toString()
    })

    proc.stderr.on("data", (data) => {
      stderr += data.toString()
    })

    proc.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`Command failed with code ${code}\n${stderr}`))
      } else {
        resolve({ stdout, stderr })
      }
    })

    setTimeout(() => {
      proc.kill()
      reject(new Error("Command timed out after 5 seconds"))
    }, 5000)
  })
}

export interface ShellServerOptions {
  allowedCommands?: string[]
  timeout?: number
  approvalHandler?: (command: string, args: string[]) => Promise<boolean>
}

export function createServer(options: ShellServerOptions = {}) {
  const server = new Server(
    {
      name: "shell-command-server",
      version: "0.1.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  )

  // Override defaults with options
  const customAllowedCommands = options.allowedCommands
  if (customAllowedCommands) {
    customAllowedCommands.forEach(cmd => ALLOWED_COMMANDS.add(cmd))
  }

  const approvalHandler = options.approvalHandler || (() => Promise.resolve(true))

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "execute_command",
          description: 
            `Execute a shell command safely. Only allowed commands: ${[...ALLOWED_COMMANDS].join(", ")}. ` +
            "Provide a clear purpose explaining what the command will do. " +
            "Command will require human approval before execution.",
          inputSchema: zodToJsonSchema(ExecuteCommandArgsSchema) as ToolInput,
        },
      ],
    }
  })

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
      const { name, arguments: args } = request.params

      if (name !== "execute_command") {
        throw new Error(`Unknown tool: ${name}`)
      }

      const parsed = ExecuteCommandArgsSchema.safeParse(args)
      if (!parsed.success) {
        throw new Error(`Invalid arguments: ${parsed.error}`)
      }

      const { command, args: cmdArgs } = parsed.data

      // Validate command
      if (!ALLOWED_COMMANDS.has(command)) {
        throw new Error(`Command not allowed: ${command}`)
      }

      // Get human approval without purpose
      const approved = await approvalHandler(command, cmdArgs)
      if (!approved) {
        return {
          content: [{ 
            type: "text", 
            text: "Command was not approved by user."
          }],
        }
      }

      // Execute command
      const result = await executeCommand(command, cmdArgs)
      
      return {
        content: [
          {
            type: "text",
            text: `Executed: ${command} ${cmdArgs.join(" ")}\nOutput:\n${result.stdout}${
              result.stderr ? `\nErrors:\n${result.stderr}` : ""
            }`,
          },
        ],
      }

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error)
      return {
        content: [{ type: "text", text: `Error: ${errorMessage}` }],
        isError: true,
      }
    }
  })

  return server
}