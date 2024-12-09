import * as agent from "@unroute/mcp-agent"
import * as exa from "@unroute/mcp-exa"
import * as fs from "@unroute/mcp-fs"
import { Connection } from "@unroute/sdk"
import dotenv from "dotenv"
import path from "node:path"
import readline from "node:readline"
dotenv.config()

// const trace = langfuse.trace({
// 	name: "blacksmith-cli",
// })

const systemPrompt = `\
You are a Typescript SDK generation agent. You aim is to generate a Model Context Protocol (MCP) npm library from API documentation. MCP is a protocol that enables secure connections between host applications and services. Full documentation at https://modelcontextprotocol.io/llms.txt.

You will have access to a list of existing MCPs in the "mcps/" directory, which you should use as reference on how to write an MCP.
You should delegate sub-tasks by invoking an LLM-agent. Delegating subtasks makes your job easier as you don't have to put worry about too many things at once.
Your MCP should be up to date to the latest version of any given API, which is available online. Make sure you do your research to figure out how to build MCP correctly. Recalling this from your memory without research is error-prone.

A well written MCP package:
- defines and exports a schema for the API using Zod
- exports a \`createServer\` function that takes a list of tools and returns an object of type \`Server\` from "@modelcontextprotocol/sdk/server/index.js".
- ensures the \`createServer\` function takes an optional parameter for any authentication if relevant. The server could be hosted elsewhere and not be accessible to the client, so the client will need to be able to pass in the API key to the server upon loading. The \`exa\` server has a good example of this.

Your output artifact should be a fully functional Typescript npm package that is installable with \`npm install\`.
`

// Add function to get user input
async function getUserInput(): Promise<string> {
	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout,
	})

	return new Promise((resolve) => {
		rl.question("You: ", (input) => {
			rl.close()
			resolve(input)
		})
	})
}

async function main() {
	// Create MCP servers first
	const fsServer = fs.createServer({
		allowedDirectories: [
			path.join(process.cwd(), "..", "typescript-sdk", "mcps"),
		],
	})

	const exaServer = exa.createServer()

	// Check if API key is defined
	const apiKey = process.env.ANTHROPIC_API_KEY;
	console.log("API Key:", apiKey);
	if (!apiKey) {
		console.error("Error: ANTHROPIC_API_KEY is not defined.");
		return;
	}

	// Clean, intuitive configuration
	const connection = await Connection.connect({
		agent: agent.createServer(
			{
				fs: fsServer,
				exa: exaServer,
			},
			{
				apiKey: apiKey,
				maxTokens: 4096,
			},
		),
	})
	try {
		console.log("What MCP are you trying to build? Describe in detail:")

		while (true) {
			const userPrompt = await getUserInput()
			if (!userPrompt) {
				console.log("exiting...")
				return
			}
			let response = await connection.callTools([
				{
					mcp: "agent",
					name: "run",
					arguments: {
						instruction: `${systemPrompt}\n${userPrompt}`,
					},
				},
			])

			console.log(JSON.stringify(response, null, 2))
			response = await connection.callTools(
				[
					{
						mcp: "agent",
						name: "get_result",
						arguments: {
							pid: JSON.parse((response[0].content as any)[0].text).pid,
							block: 60 * 10,
						},
					},
				],
				{
					timeout: 60 * 10 * 1000,
				},
			)
			console.log(JSON.stringify(response, null, 2))
		}
	} finally {
		// Remove this line:
		// await langfuse.shutdownAsync()
	}
}

main()