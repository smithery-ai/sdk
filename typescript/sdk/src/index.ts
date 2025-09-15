// Smithery SDK – Barrel file
// Central re-exports so that `dist/index.js` & `index.d.ts` are generated.
// Update this list whenever a new top-level feature is added.

// Shared utilities
export * from "./shared/config.js"
export * from "./shared/patch.js"

// Client-side helpers

export * from "./client/transport.js"
export * from "./client/integrations/wrap-error.js"

// Server-side helpers (selective to avoid duplicate type names)
export {
	createStatefulServer,
	type StatefulServerOptions,
} from "./server/stateful.js"
export * from "./server/session.js"
