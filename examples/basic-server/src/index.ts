import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"

// Optional: If you have user-level config, define it here
export const configSchema = z.object({
	debug: z.boolean().default(false).describe("Enable debug logging"),
})

export default function createServer({
	config,
}: {
	config: z.infer<typeof configSchema> // your server configuration
}) {
	const server = new McpServer({
		name: "Say Hello",
		version: "1.0.0",
	})

	// Add a tool
	server.registerTool(
		"hello",
		{
			title: "Hello Tool",
			description: "Say hello to someone",
			inputSchema: { name: z.string().describe("Name to greet") },
		},
		async ({ name }) => ({
			content: [
				{ 
					type: "text", 
					text: config.debug ? `DEBUG: Hello ${name}` : `Hello, ${name}!` // use provided config
				}
			],
		}),
	)

	// Add a resource
	server.registerResource(
		"hello-world-history",
		"history://hello-world",
		{
			title: "Hello World History",
			description: "The origin story of the famous 'Hello, World' program",
		},
		async uri => ({
			contents: [
				{
					uri: uri.href,
					text: '"Hello, World" first appeared in a 1972 Bell Labs memo by Brian Kernighan and later became the iconic first program for beginners in countless languages.',
					mimeType: "text/plain",
				},
			],
		}),
	)

	// Add a prompt
	server.registerPrompt(
		"greet",
		{
			title: "Hello Prompt",
			description: "Say hello to someone",
			argsSchema: {
				name: z.string().describe("Name of the person to greet"),
			},
		},
		async ({ name }) => {
			return {
				messages: [
					{
						role: "user",
						content: {
							type: "text",
							text: `Say hello to ${name}`,
						},
					},
				],
			}
		},
	)

	return server.server
}
