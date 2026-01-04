/**
 * Config - loaded from smithery.config.ts
 */
export interface Config {
	build?: {
		/**
		 * Path to the server's entry point.
		 * Default: detected from package.json "module" or "main"
		 */
		entry?: string
		/**
		 * Optional esbuild overrides for bundling
		 */
		esbuild?: Record<string, unknown>
	}
}
