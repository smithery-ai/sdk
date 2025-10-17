// Smithery SDK – Main exports
// Use subpath imports for tree-shaking: @smithery/sdk/server, /helpers, /react

// === Shared Utilities ===
export * from "./shared/config.js"
export * from "./shared/patch.js"

// === Server Primitives ===
// Stateful/stateless server patterns, session management, auth
export {
	createStatefulServer,
	type StatefulServerOptions,
} from "./server/stateful.js"
export * from "./server/session.js"
export * from "./server/auth/identity.js"
export * from "./server/auth/oauth.js"

// === Widget SDK - Server ===
// createWidgetServer() - MCP server wrapper for widgets
export { createWidgetServer } from "./server/widget.js"
export type { WidgetServerOptions } from "./server/widget.js"

// === Widget SDK - Helpers ===
// widget.response() - Standard success response
// widget.error() - Standard error response  
// widget.resource() - Auto-generate widget HTML
export { widget } from "./helpers/index.js"
export type {
	WidgetToolOptions,
	WidgetResponseOptions,
	WidgetResourceOptions,
} from "./helpers/index.js"

// === Widget SDK - React Types ===
// Common types re-exported for convenience (full hooks in @smithery/sdk/react)
export type {
	Theme,
	DisplayMode,
	OpenAiGlobals,
	CallToolResponse,
} from "./react/types.js"
