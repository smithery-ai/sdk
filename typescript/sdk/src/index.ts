// Smithery SDK – Main exports
// Use subpath imports for tree-shaking: @smithery/sdk/server, /helpers

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
