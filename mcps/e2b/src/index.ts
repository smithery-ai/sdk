import { Sandbox } from '@e2b/code-interpreter'
import { Server } from '@modelcontextprotocol/sdk/server/index'
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
  RequestSchema,
  ResultSchema,
} from '@modelcontextprotocol/sdk/types'
import { z } from 'zod'
import { zodToJsonSchema } from 'zod-to-json-schema'

const toolSchema = z.object({
  code: z.string(),
})

export const AuthRequestSchema = RequestSchema.extend({
  method: z.literal('auth'),
  params: z.object({
    apiKey: z.string(),
  }),
})
export const AuthResultSchema = ResultSchema.extend({})

class E2BServer {
  server: Server
  private sandbox?: Sandbox

  constructor() {
    this.server = new Server(
      {
        name: 'e2b-mcp-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      },
    )

    this.server.setRequestHandler(AuthRequestSchema, async (request) => {
      const { apiKey } = request.params
      this.sandbox = await Sandbox.create({
        apiKey,
      })
      return {}
    })

    this.server.onclose = () => {
      this.sandbox?.kill()
    }

    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'run_code',
          description:
            'Run python code in a secure sandbox by E2B. Using the Jupyter Notebook syntax.',
          inputSchema: zodToJsonSchema(toolSchema),
        },
      ],
    }))

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (!this.sandbox) {
        throw new Error('Unrecoverable error: Not authenticated.')
      }

      if (request.params.name !== 'run_code') {
        throw new McpError(
          ErrorCode.MethodNotFound,
          `Unknown tool: ${request.params.name}`,
        )
      }

      const parsed = toolSchema.safeParse(request.params.arguments)
      if (!parsed.success) {
        throw new McpError(
          ErrorCode.InvalidParams,
          'Invalid code interpreter arguments',
        )
      }

      const { code } = parsed.data
      const { results, logs } = await this.sandbox.runCode(code)

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              output: results,
              logs,
            }),
          },
        ],
      }
    })
  }
}

export function createServer() {
  return new E2BServer().server
}
