import type express from "express"
import type { OAuthServerProvider } from "@modelcontextprotocol/sdk/server/auth/provider.js"
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js"
import { mcpAuthRouter } from "@modelcontextprotocol/sdk/server/auth/router.js"
import type { Response } from "express"

/**
 * OAuth server provider that supports a callback handler.
 * The callback handler is invoked to catch the OAuth callback from the OAuth provider.
 */
export interface CallbackOAuthServerProvider extends OAuthServerProvider {
	/** Provider-specific callback handler used by the SDK */
	handleOAuthCallback?: (
		code: string,
		state: string | undefined,
		res: Response,
	) => Promise<URL>
	// Path to mount the OAuth routes. Default is "/"
	basePath?: string
	// The path OAuth will redirect to after authentication. Typically "/callback"
	callbackPath: string
}

export function mountOAuth(
	app: express.Application,
	provider: CallbackOAuthServerProvider,
) {
	// Mount OAuth authorization and token routes with dynamic issuer URL and provider
	app.use(provider.basePath ?? "/", (req, res, next) => {
		const host = req.get("host") ?? "localhost"
		// Issuer URL must be https
		const issuerUrl = new URL(`https://${host}`)
		const router = mcpAuthRouter({ provider, issuerUrl })
		return router(req, res, next)
	})

	const callbackHandler = provider.handleOAuthCallback
	if (callbackHandler) {
		// Callback handler
		app.get(provider.callbackPath, async (req, res) => {
			const code =
				typeof req.query.code === "string" ? req.query.code : undefined
			const state =
				typeof req.query.state === "string" ? req.query.state : undefined
			if (!code) {
				res.status(400).send("Invalid request parameters")
				return
			}
			try {
				const redirectUrl = await callbackHandler.bind(provider)(
					code,
					state,
					res,
				)
				res.redirect(redirectUrl.toString())
			} catch (error) {
				console.error(error)
				res.status(500).send("Error during authentication callback")
			}
		})
	}
	// Bearer protection for all /mcp routes (POST/GET/DELETE)
	app.use("/mcp", (req, res, next) => {
		return requireBearerAuth({ verifier: provider })(req, res, next)
	})
}
