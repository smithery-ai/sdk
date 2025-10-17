import { readFile } from "node:fs/promises"
import { resolve } from "node:path"
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"

export interface WidgetResponseOptions<TState = Record<string, unknown>> {
	structuredData: TState
	message: string
	meta?: Record<string, unknown>
}

export interface WidgetResourceOptions {
	name: string
	description?: string
	prefersBorder?: boolean
	csp?: {
		connect_domains?: string[]
		resource_domains?: string[]
	}
	bundlePath?: string
	bundleURL?: string
	cssURLs?: string | string[]
}

export interface WidgetToolOptions {
	template: string
	invoking?: string
	invoked?: string
	widgetAccessible?: boolean
}

export interface WidgetErrorOptions {
	message: string
	details?: unknown
	meta?: Record<string, unknown>
}

export function response<TState = Record<string, unknown>>(
	options: WidgetResponseOptions<TState>,
) {
	const { structuredData, message, meta = {} } = options

	return {
		structuredContent: structuredData as Record<string, unknown>,
		content: [
			{
				type: "text" as const,
				text: message,
			},
		],
		_meta: meta,
	}
}

export function error(options: string | WidgetErrorOptions) {
	const isString = typeof options === "string"
	const message = isString ? options : options.message
	const details = isString ? undefined : options.details
	const meta = isString ? undefined : options.meta

	const finalMeta: Record<string, unknown> = {
		...(meta || {}),
	}

	if (details) {
		finalMeta.errorDetails = details
	}

	return {
		content: [
			{
				type: "text" as const,
				text: message,
			},
		],
		isError: true,
		...(Object.keys(finalMeta).length > 0 && { _meta: finalMeta }),
	}
}

export function resource<TState = Record<string, unknown>>(
	options: WidgetResourceOptions,
): {
	name: string
	uri: string
	handler: () => Promise<{
		contents: Array<{
			uri: string
			text: string
			mimeType: "text/html+skybridge"
			_meta?: Record<string, unknown>
		}>
	}>
	toolConfig: (
		options?: Omit<WidgetToolOptions, "template">,
	) => Record<string, unknown>
	response: (
		options: WidgetResponseOptions<TState>,
	) => ReturnType<typeof response<TState>>
	register: (server: Pick<McpServer, "registerResource">) => void
} {
	const {
		name,
		description,
		prefersBorder,
		csp,
		bundlePath = `.smithery/${name}.js`,
		bundleURL,
	} = options

	const uri = `ui://widget/${name}.html`

	const handler = async () => {
		let scriptTag: string

		if (bundleURL) {
			scriptTag = `<script type="module" src="${bundleURL}"></script>`
		} else {
			const js = await readFile(resolve(process.cwd(), bundlePath), "utf-8")
			scriptTag = `<script type="module">${js}</script>`
		}

		const cssUrls = Array.isArray(options.cssURLs)
			? options.cssURLs
			: options.cssURLs
				? [options.cssURLs]
				: []
		const cssLinks = cssUrls
			.map(url => `<link rel="stylesheet" href="${url}">`)
			.join("\n")

		const html = `
<div id="${name}-root"></div>
${cssLinks}
${scriptTag}
    `.trim()

		const _meta: Record<string, unknown> = {}
		if (description) _meta["openai/widgetDescription"] = description
		if (prefersBorder !== undefined)
			_meta["openai/widgetPrefersBorder"] = prefersBorder
		if (csp) _meta["openai/widgetCSP"] = csp

		return {
			contents: [
				{
					uri,
					text: html,
					mimeType: "text/html+skybridge" as const,
					...(Object.keys(_meta).length > 0 && { _meta }),
				},
			],
		}
	}

	const toolConfig = (options?: Omit<WidgetToolOptions, "template">) => {
		return {
			"openai/outputTemplate": uri,
			"openai/widgetAccessible": options?.widgetAccessible ?? true,
			...(options?.invoking && {
				"openai/toolInvocation/invoking": options.invoking,
			}),
			...(options?.invoked && {
				"openai/toolInvocation/invoked": options.invoked,
			}),
		}
	}

	const typedResponse = (options: WidgetResponseOptions<TState>) => {
		return response<TState>(options)
	}

	const register = (server: Pick<McpServer, "registerResource">) => {
		server.registerResource(name, uri, {}, handler)
	}

	return {
		name,
		uri,
		handler,
		toolConfig,
		response: typedResponse,
		register,
	}
}

export function toolConfig(
	options: WidgetToolOptions,
): Record<string, unknown> {
	const meta: Record<string, unknown> = {
		"openai/outputTemplate": `ui://widget/${options.template}.html`,
		"openai/widgetAccessible": options.widgetAccessible ?? true,
	}

	if (options.invoking) {
		meta["openai/toolInvocation/invoking"] = options.invoking
	}

	if (options.invoked) {
		meta["openai/toolInvocation/invoked"] = options.invoked
	}

	return meta
}

export const widget = {
	response,
	error,
	resource,
	toolConfig,
}
