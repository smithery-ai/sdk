import type { z } from "zod"

export interface WidgetToolOptions {
  accessible?: boolean
  template?: string
  invoking?: string
  invoked?: string
}

export interface ToolConfig {
  title: string
  description: string
  inputSchema: Record<string, z.ZodType>
  widget?: WidgetToolOptions
}

export function tool(config: ToolConfig) {
  const { title, description, inputSchema, widget: widgetOptions } = config

  const _meta: Record<string, unknown> = {}

  if (widgetOptions) {
    if (widgetOptions.accessible !== undefined) {
      _meta["openai/widgetAccessible"] = widgetOptions.accessible
    }

    if (widgetOptions.template) {
      _meta["openai/outputTemplate"] = `ui://widget/${widgetOptions.template}.html`
    }

    if (widgetOptions.invoking) {
      _meta["openai/toolInvocation/invoking"] = widgetOptions.invoking
    }

    if (widgetOptions.invoked) {
      _meta["openai/toolInvocation/invoked"] = widgetOptions.invoked
    }
  }

  return {
    title,
    description,
    inputSchema,
    _meta: Object.keys(_meta).length > 0 ? _meta : undefined,
  }
}

