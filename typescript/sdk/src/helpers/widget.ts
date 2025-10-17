import { readFile } from "node:fs/promises"
import { resolve } from "node:path"

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
  bundle?: string
  bundleCSS?: string | string[]
}

export interface WidgetToolOptions {
  template: string
  invoking?: string
  invoked?: string
  widgetAccessible?: boolean
}

export function response<TState = Record<string, unknown>>(
  options: WidgetResponseOptions<TState>
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

export function error(message: string, details?: unknown) {
  return {
    content: [
      {
        type: "text" as const,
        text: message,
      },
    ],
    isError: true,
    _meta: details ? { errorDetails: details } : undefined,
  }
}

export function resource<TState = Record<string, unknown>>(options: WidgetResourceOptions): {
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
  toolConfig: (options?: Omit<WidgetToolOptions, "template">) => Record<string, unknown>
  response: (options: WidgetResponseOptions<TState>) => ReturnType<typeof response<TState>>
  register: (server: { registerResource: (name: string, uri: string, metadata: Record<string, unknown>, handler: () => Promise<{ contents: Array<{ uri: string; text: string; mimeType: string; _meta?: Record<string, unknown> }> }>) => void }) => void
} {
  const { name, description, prefersBorder, csp, bundle = `.smithery/${name}.js` } = options

  const uri = `ui://widget/${name}.html`

  const handler = async () => {
    const js = await readFile(resolve(process.cwd(), bundle), "utf-8")

    const cssUrls = Array.isArray(options.bundleCSS) ? options.bundleCSS : (options.bundleCSS ? [options.bundleCSS] : [])
    const cssLinks = cssUrls.map(url => `<link rel="stylesheet" href="${url}">`).join('\n')

    const html = `
<div id="${name}-root"></div>
${cssLinks}
<script type="module">${js}</script>
    `.trim()

    const _meta: Record<string, unknown> = {}
    if (description) _meta["openai/widgetDescription"] = description
    if (prefersBorder !== undefined) _meta["openai/widgetPrefersBorder"] = prefersBorder
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
      ...(options?.invoking && { "openai/toolInvocation/invoking": options.invoking }),
      ...(options?.invoked && { "openai/toolInvocation/invoked": options.invoked }),
    }
  }

  const typedResponse = (options: WidgetResponseOptions<TState>) => {
    return response<TState>(options)
  }

  const register = (server: { registerResource: (name: string, uri: string, metadata: Record<string, unknown>, handler: () => Promise<{ contents: Array<{ uri: string; text: string; mimeType: string; _meta?: Record<string, unknown> }> }>) => void }) => {
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

export function toolConfig(options: WidgetToolOptions): Record<string, unknown> {
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

