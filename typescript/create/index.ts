#!/usr/bin/env node

import { $ } from "execa"
import inquirer from "inquirer"
import { Command } from "commander"
import boxen from "boxen"
import chalk from "chalk"
import figlet from "figlet"

function detectPackageManager(): string {
	const userAgent = process.env.npm_config_user_agent

	if (userAgent) {
		if (userAgent.startsWith("yarn")) return "yarn"
		if (userAgent.startsWith("pnpm")) return "pnpm"
		if (userAgent.startsWith("bun")) return "bun"
		if (userAgent.startsWith("npm")) return "npm"
	}

	return "npm"
}

// Establish CLI args/flags
const program = new Command()
program.argument("[projectName]", "Name of the project").parse(process.argv)
program.option("--package-manager", "Package manager to use")

let [projectName] = program.args
const packageManager = program.opts().packageManager || detectPackageManager()

// If no project name is provided, prompt the user for it
if (!projectName) {
	const { projectName: promptedName } = await inquirer.prompt([
		{
			type: "input",
			name: "projectName",
			message: "What is your project name?",
			validate: (input: string) => {
				if (!input.trim()) {
					return "Project name cannot be empty"
				}
				return true
			},
		},
	])
	// Use the prompted name
	console.log(`Creating project: ${promptedName}`)
	projectName = promptedName
} else {
	// Use the provided name
	console.log(`Creating project: ${projectName}`)
}

async function load<T>(
	startMsg: string,
	endMsg: string,
	command: () => Promise<T>,
): Promise<T> {
	process.stdout.write(`[ ] ${startMsg}\r`)
	const loadingChars = ["|", "/", "-", "\\"]
	let i = 0
	const loadingInterval = setInterval(() => {
		process.stdout.write(`[${loadingChars[i]}] ${startMsg}\r`)
		i = (i + 1) % loadingChars.length
	}, 250)

	const result = await command()
	clearInterval(loadingInterval)
	process.stdout.write(`\r\x1b[K[\u2713] ${endMsg}\n`)
	return result
}

await load("Cloning scaffold from GitHub...", "Scaffold cloned", async () => {
	// Clone the scaffold and only keep the scaffold directory
	await $`git clone https://github.com/smithery-ai/sdk.git ${projectName}`
	const files = await $`shx ls -al ${projectName}`
	for (const file of files.stdout.split("\n")) {
		const fileName = file.split(" ").pop()
		if (
			fileName &&
			fileName !== "typescript" &&
			fileName !== "." &&
			fileName !== ".."
		) {
			await $`shx rm -rf ${projectName}/${fileName}`
		}
	}
	await $`shx cp -r ${projectName}/typescript/create/scaffold/. ${projectName}/`
	await $`shx rm -rf ${projectName}/typescript`
})

await load("Navigating to project...", "Project navigated", async () => {
	// await $`cd ${projectName}`; Not needed - we use cwd option instead
})
await $`shx rm -rf ${projectName}/.git`
await $`shx rm -rf ${projectName}/package-lock.json`
await $`shx rm -rf ${projectName}/node_modules`

await load("Installing dependencies...", "Dependencies installed", async () => {
	console.log("\n\n")
	await $({ cwd: projectName, stdio: "inherit" })`${packageManager} install`
})

// Generate ASCII art for "Smithery" using figlet
const asciiArt = figlet.textSync("Smithery", { font: "Sub-Zero" })

console.log(
	"\n\n\n" +
		boxen(
			`${chalk.blue.bold(asciiArt)}\n\n${chalk.green.bold("* Welcome to your MCP server!")}\n\nTo get started, run:\n\n${chalk.rgb(
				234,
				88,
				12,
			)(
				`cd ${projectName} && ${packageManager} run dev`,
			)}\n\nTry saying something like ${chalk.cyan.bold("'Say hello to John'")}`,
			{
				padding: 2,
				textAlignment: "left",
				borderStyle: "round",
				borderColor: "blue",
				title: chalk.blue.bold("Smithery MCP Server"),
				titleAlignment: "left",
			},
		),
)
