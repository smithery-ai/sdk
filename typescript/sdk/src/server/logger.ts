import chalk from "chalk"

/**
 * Logger interface for structured logging
 */
export interface Logger {
	info(msg: string, ...args: unknown[]): void
	info(obj: Record<string, unknown>, msg?: string, ...args: unknown[]): void
	error(msg: string, ...args: unknown[]): void
	error(obj: Record<string, unknown>, msg?: string, ...args: unknown[]): void
	warn(msg: string, ...args: unknown[]): void
	warn(obj: Record<string, unknown>, msg?: string, ...args: unknown[]): void
	debug(msg: string, ...args: unknown[]): void
	debug(obj: Record<string, unknown>, msg?: string, ...args: unknown[]): void
}

type LogLevel = "debug" | "info" | "warn" | "error"

/**
 * Lightweight stringify with depth limiting
 */
function stringifyWithDepth(obj: unknown, maxDepth = 3): string {
	let depth = 0
	const seen = new WeakSet()

	try {
		return JSON.stringify(
			obj,
			(key, value) => {
				// Track depth
				if (key === "") depth = 0
				else if (typeof value === "object" && value !== null) depth++

				// Depth limit
				if (depth > maxDepth) {
					return "[Object]"
				}

				// Circular reference check
				if (typeof value === "object" && value !== null) {
					if (seen.has(value)) return "[Circular]"
					seen.add(value)
				}

				// Handle special types
				if (typeof value === "function") return "[Function]"
				if (typeof value === "bigint") return `${value}n`
				if (value instanceof Error)
					return { name: value.name, message: value.message }
				if (value instanceof Date) return value.toISOString()

				return value
			},
			2,
		)
	} catch {
		return String(obj)
	}
}

/**
 * Creates a simple console-based logger with pretty formatting
 */
export function createLogger(logLevel: LogLevel = "info"): Logger {
	const levels = { debug: 0, info: 1, warn: 2, error: 3 }
	const currentLevel = levels[logLevel]

	const formatLog = (
		level: string,
		color: (str: string) => string,
		msgOrObj: unknown,
		msg?: string,
	) => {
		const time = new Date().toISOString().split("T")[1].split(".")[0]
		const timestamp = chalk.dim(time)
		const levelStr = color(level)

		if (typeof msgOrObj === "string") {
			return `${timestamp} ${levelStr} ${msgOrObj}`
		}
		const message = msg || ""
		const data = stringifyWithDepth(msgOrObj, 3)
		return `${timestamp} ${levelStr} ${message}\n${chalk.dim(data)}`
	}

	return {
		debug: (msgOrObj: unknown, msg?: string) => {
			if (currentLevel <= 0)
				console.error(formatLog("DEBUG", chalk.cyan, msgOrObj, msg))
		},
		info: (msgOrObj: unknown, msg?: string) => {
			if (currentLevel <= 1)
				console.error(formatLog("INFO", chalk.blue, msgOrObj, msg))
		},
		warn: (msgOrObj: unknown, msg?: string) => {
			if (currentLevel <= 2)
				console.error(formatLog("WARN", chalk.yellow, msgOrObj, msg))
		},
		error: (msgOrObj: unknown, msg?: string) => {
			if (currentLevel <= 3)
				console.error(formatLog("ERROR", chalk.red, msgOrObj, msg))
		},
	} as Logger
}
