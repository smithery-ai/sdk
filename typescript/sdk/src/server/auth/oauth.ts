import type {
	OAuthServerProvider,
	OAuthTokenVerifier,
} from "@modelcontextprotocol/sdk/server/auth/provider.js"
import type { Application, Response } from "express"
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js"
import {
	mcpAuthMetadataRouter,
	createOAuthMetadata,
} from "@modelcontextprotocol/sdk/server/auth/router.js"
import { authorizationHandler } from "@modelcontextprotocol/sdk/server/auth/handlers/authorize.js"
import { tokenHandler } from "@modelcontextprotocol/sdk/server/auth/handlers/token.js"
import { clientRegistrationHandler } from "@modelcontextprotocol/sdk/server/auth/handlers/register.js"
import { revocationHandler } from "@modelcontextprotocol/sdk/server/auth/handlers/revoke.js"
import { metadataHandler } from "@modelcontextprotocol/sdk/server/auth/handlers/metadata.js"
import type {
	OAuthMetadata,
	OAuthProtectedResourceMetadata,
} from "@modelcontextprotocol/sdk/shared/auth.js"
import { mountIdentity, type IdentityHandler } from "./identity.js"

export interface CallbackOAuthServerProvider extends OAuthServerProvider {
	basePath?: string
	callbackPath?: string
	handleOAuthCallback?: (
		code: string,
		state: string | undefined,
		res: Response,
	) => Promise<URL>
}

export interface OAuthMountOptions {
	provider?: CallbackOAuthServerProvider | OAuthTokenVerifier
	identity?: IdentityHandler
}

function isOAuthProvider(
	provider: CallbackOAuthServerProvider | OAuthTokenVerifier | undefined,
): provider is CallbackOAuthServerProvider {
	return !!provider && "authorize" in provider
}

export function mountOAuth(app: Application, opts: OAuthMountOptions) {
	// Determine base path once based on OAuth provider or identity
	const provider = opts.provider
	const hasOAuth = isOAuthProvider(provider)
	const rawBasePath = hasOAuth
		? (provider.basePath ?? "/")
		: (opts.identity?.basePath ?? "/")
	const basePath = rawBasePath.endsWith("/") ? rawBasePath : `${rawBasePath}/`

	// Precompute endpoint pathnames from metadata
	let authorizationPath: string | undefined
	let tokenPath: string | undefined
	let registrationPath: string | undefined
	let revocationPath: string | undefined

	if (isOAuthProvider(provider)) {
		const placeholderIssuer = new URL("https://localhost")
		const placeholderBaseUrl = new URL(basePath, placeholderIssuer)
		const localMetadata = createOAuthMetadata({
			provider,
			issuerUrl: placeholderIssuer,
			baseUrl: placeholderBaseUrl,
		})
		authorizationPath = new URL(localMetadata.authorization_endpoint).pathname
		tokenPath = new URL(localMetadata.token_endpoint).pathname
		if (localMetadata.registration_endpoint) {
			registrationPath = new URL(localMetadata.registration_endpoint).pathname
		}
		if (localMetadata.revocation_endpoint) {
			revocationPath = new URL(localMetadata.revocation_endpoint).pathname
		}
	}

	// Metadata endpoints
	if (isOAuthProvider(provider)) {
		// Mount a per-request adapter so issuer/baseUrl reflect Host/Proto
		app.use((req, res, next) => {
			if (!req.path.startsWith("/.well-known/")) return next()
			const host = req.get("host") ?? "localhost"

			if (req.protocol !== "https") {
				console.warn(
					"Detected http but using https for issuer URL in OAuth metadata since it will fail otherwise.",
				)
			}
			const issuerUrl = new URL(`https://${host}`)
			const baseUrl = new URL(basePath, issuerUrl)
			const oauthMetadata: OAuthMetadata = createOAuthMetadata({
				provider,
				issuerUrl,
				baseUrl,
			})
			if (opts.identity) {
				oauthMetadata.grant_types_supported = Array.from(
					new Set([
						...(oauthMetadata.grant_types_supported ?? []),
						"urn:ietf:params:oauth:grant-type:jwt-bearer",
					]),
				)
			}
			const resourceServerUrl = new URL("/mcp", issuerUrl)
			const metadataRouter = mcpAuthMetadataRouter({
				oauthMetadata,
				resourceServerUrl,
			})
			return metadataRouter(req, res, next)
		})
	} else if (opts.identity) {
		// Identity-only: explicitly mount protected resource metadata endpoint
		app.use("/.well-known/oauth-protected-resource", (req, res, next) => {
			const host = req.get("host") ?? "localhost"
			const issuerUrl = new URL(`${req.protocol}://${host}`)
			const protectedResourceMetadata: OAuthProtectedResourceMetadata = {
				resource: new URL("/mcp", issuerUrl).href,
				authorization_servers: [issuerUrl.href],
			}
			return metadataHandler(protectedResourceMetadata)(req, res, next)
		})

		// Identity-only: also advertise minimal AS metadata for discovery per RFC 8414
		app.use("/.well-known/oauth-authorization-server", (req, res, next) => {
			const host = req.get("host") ?? "localhost"
			const issuerUrl = new URL(`${req.protocol}://${host}`)
			const oauthMetadata: Omit<OAuthMetadata, "authorization_endpoint"> = {
				issuer: issuerUrl.href,
				token_endpoint: new URL(`${basePath}token`, issuerUrl).href,
				grant_types_supported: ["urn:ietf:params:oauth:grant-type:jwt-bearer"],
			}
			return metadataHandler(oauthMetadata as OAuthMetadata)(req, res, next)
		})
	}

	// Mount identity (JWT bearer grant) first so OAuth token can fall through
	if (opts.identity) {
		const identityOptions = {
			...opts.identity,
			basePath,
			tokenPath: tokenPath ?? `${basePath}token`,
		}
		mountIdentity(app, identityOptions)
	}

	// Mount OAuth endpoints functionally if an OAuth provider is present
	if (isOAuthProvider(provider)) {
		// Authorization endpoint
		const authPath = authorizationPath ?? `${basePath}authorize`
		app.use(authPath, authorizationHandler({ provider }))

		// Token endpoint (OAuth); identity's token handler will handle JWT grant and call next() otherwise
		const tokPath = tokenPath ?? `${basePath}token`
		app.use(tokPath, tokenHandler({ provider }))

		// Dynamic client registration if supported
		if (provider.clientsStore?.registerClient) {
			const regPath = registrationPath ?? `${basePath}register`
			app.use(
				regPath,
				clientRegistrationHandler({ clientsStore: provider.clientsStore }),
			)
		}

		// Token revocation if supported
		if (provider.revokeToken) {
			const revPath = revocationPath ?? `${basePath}revoke`
			app.use(revPath, revocationHandler({ provider }))
		}

		// Optional OAuth callback
		const callbackHandler = provider.handleOAuthCallback?.bind(provider)
		if (callbackHandler) {
			const callbackPath = provider.callbackPath ?? "/callback"
			app.get(callbackPath, async (req, res) => {
				const code =
					typeof req.query.code === "string" ? req.query.code : undefined
				const state =
					typeof req.query.state === "string" ? req.query.state : undefined
				if (!code) {
					res.status(400).send("Invalid request parameters")
					return
				}
				try {
					const redirectUrl = await callbackHandler(code, state, res)
					res.redirect(redirectUrl.toString())
				} catch (error) {
					console.error(error)
					res.status(500).send("Error during authentication callback")
				}
			})
		}
	}

	// Protect MCP resource with bearer auth if a verifier/provider is present
	if (provider) {
		app.use("/mcp", (req, res, next) => {
			return requireBearerAuth({
				verifier: provider,
			})(req, res, next)
		})
	}
}
