import { readFile } from "node:fs/promises"
import { resolve } from "node:path"

export interface WidgetResponseOptions {
  state: Record<string, unknown>
  message: string
  meta?: Record<string, unknown>
}

export interface WidgetResourceOptions {
  name: string
  description: string
  bundle: string
  prefersBorder?: boolean
  csp?: {
    connect?: string[]
    resources?: string[]
  }
}

export interface WidgetToolOptions {
  template: string
  invoking?: string
  invoked?: string
}

export function response(options: WidgetResponseOptions) {
  const { state, message, meta = {} } = options

  return {
    structuredContent: state as Record<string, unknown>,
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

export function resource(options: WidgetResourceOptions) {
  const { name, description, bundle, prefersBorder, csp } = options

  const uri = `ui://widget/${name}.html`

  const handler = async () => {
    const js = await readFile(resolve(process.cwd(), bundle), "utf-8")

    const html = `
<div id="${name}-root"></div>
<script type="module">${js}</script>
    `.trim()

    const resourceMeta: Record<string, unknown> = {
      "openai/widgetDescription": description,
    }

    if (prefersBorder !== undefined) {
      resourceMeta["openai/widgetPrefersBorder"] = prefersBorder
    }

    if (csp) {
      resourceMeta["openai/widgetCSP"] = {
        connect_domains: csp.connect ?? [],
        resource_domains: csp.resources ?? [],
      }
    }

    return {
      contents: [
        {
          uri,
          text: html,
          mimeType: "text/html+skybridge" as const,
          _meta: resourceMeta,
        },
      ],
    }
  }

  return { uri, metadata: { title: `${name} Widget`, description }, handler }
}

export function toolConfig(options: WidgetToolOptions): Record<string, unknown> {
  const meta: Record<string, unknown> = {
    "openai/outputTemplate": `ui://widget/${options.template}.html`,
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

