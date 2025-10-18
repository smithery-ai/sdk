/**
 * Local Filesystem MCP Server
 * 
 * This server provides tools to explore the local filesystem.
 * To run your server, run "npm run dev"
 *
 * You might find these resources useful:
 *
 * MCP's TypeScript SDK (helps you define your server)
 * https://github.com/modelcontextprotocol/typescript-sdk
 *
 * smithery.yaml (defines user-level config, like settings or API keys)
 * https://smithery.ai/docs/build/project-config/smithery-yaml
 *
 * smithery CLI (run "npx @smithery/cli dev" or explore other commands below)
 * https://smithery.ai/docs/concepts/cli
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { glob } from "glob"
import { execSync } from "node:child_process"

// Optional: If you have user-level config, define it here
// This should map to the config in your smithery.yaml file
export const configSchema = z.object({
	workingDirectory: z
		.string()
		.default(process.cwd())
		.describe("Working directory for filesystem operations"),
})

export default function createServer({
	config,
}: {
	config: z.infer<typeof configSchema>
}) {
	const server = new McpServer({
		name: "Local Filesystem Explorer",
		version: "1.0.0",
	})

	// Glob tool - find files matching a pattern
	server.registerTool(
		"glob",
		{
			title: "Glob",
			description:
				"Find files matching a glob pattern (e.g., '**/*.ts', 'src/**/*.js')",
			inputSchema: {
				pattern: z
					.string()
					.describe("Glob pattern to match files (e.g., '**/*.ts')"),
			},
		},
		async ({ pattern }) => {
			try {
				const files = await glob(pattern, {
					cwd: config.workingDirectory,
					ignore: ["**/node_modules/**", "**/.git/**"],
				})

				return {
					content: [
						{
							type: "text",
							text: files.length > 0 ? files.join("\n") : "No files found",
						},
					],
				}
			} catch (error) {
				return {
					content: [
						{
							type: "text",
							text: `Error: ${error instanceof Error ? error.message : "Unknown error"}`,
						},
					],
					isError: true,
				}
			}
		},
	)

	// Grep tool - search for text in files
	server.registerTool(
		"grep",
		{
			title: "Grep",
			description: "Search for text patterns in files using grep",
			inputSchema: {
				pattern: z.string().describe("Text pattern to search for"),
				filePattern: z
					.string()
					.optional()
					.describe("Optional file pattern to limit search (e.g., '*.ts')"),
			},
		},
		async ({ pattern, filePattern }) => {
			try {
				const grepCmd = filePattern
					? `grep -r "${pattern}" --include="${filePattern}" .`
					: `grep -r "${pattern}" --exclude-dir=node_modules --exclude-dir=.git .`

				const result = execSync(grepCmd, {
					cwd: config.workingDirectory,
					encoding: "utf-8",
					maxBuffer: 10 * 1024 * 1024, // 10MB buffer
				})

				return {
					content: [
						{
							type: "text",
							text: result || "No matches found",
						},
					],
				}
			} catch (error) {
				// grep returns exit code 1 when no matches found
				if (
					error instanceof Error &&
					"status" in error &&
					error.status === 1
				) {
					return {
						content: [
							{
								type: "text",
								text: "No matches found",
							},
						],
					}
				}

				return {
					content: [
						{
							type: "text",
							text: `Error: ${error instanceof Error ? error.message : "Unknown error"}`,
						},
					],
					isError: true,
				}
			}
		},
	)

	return server.server
}

