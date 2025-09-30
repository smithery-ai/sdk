import express from "express"
import type { Application, Request, Router } from "express"
import { createRemoteJWKSet, jwtVerify, type JWTPayload } from "jose"
import type { OAuthTokens } from "@modelcontextprotocol/sdk/shared/auth.js"

export type IdentityJwtClaims = JWTPayload & Record<string, unknown>

export interface IdentityHandler {
	/** Base path to mount metadata and token endpoints. Default: "/" */
	basePath?: string
	/** Expected JWT issuer. Default: "https://server.smithery.ai" */
	issuer?: string
	/** JWKS URL for issuer. Default: "https://server.smithery.ai/.well-known/jwks.json" */
	jwksUrl?: string
	/** Optional explicit token path. Overrides basePath+"token". */
	tokenPath?: string
	/** Handle a JWT grant provided by an external identity provider (i.e., Smithery) and mint access tokens */
	handleJwtGrant: (
		claims: IdentityJwtClaims,
		req: Request,
	) => Promise<OAuthTokens | null>
}

function normalizeBasePath(basePath?: string) {
	const value = basePath ?? "/"
	return value.endsWith("/") ? value : `${value}/`
}

export function createIdentityTokenRouter(options: IdentityHandler): Router {
	const basePath = normalizeBasePath(options.basePath)
	const issuer = options.issuer ?? "https://server.smithery.ai"
	const jwksUrl = new URL(
		options.jwksUrl ?? "https://server.smithery.ai/.well-known/jwks.json",
	)

	const tokenPath =
		typeof options.tokenPath === "string" && options.tokenPath.length > 0
			? options.tokenPath
			: `${basePath}token`

	// Create JWKS resolver once; jose caches keys internally
	const JWKS = createRemoteJWKSet(jwksUrl)

	const tokenRouter = express.Router()
	// urlencoded parser required for OAuth token requests
	tokenRouter.use(express.urlencoded({ extended: false }))
	tokenRouter.post(tokenPath, async (req, res, next) => {
		try {
			const grantType =
				typeof req.body?.grant_type === "string"
					? req.body.grant_type
					: undefined
			if (grantType !== "urn:ietf:params:oauth:grant-type:jwt-bearer")
				return next()

			const assertion =
				typeof req.body?.assertion === "string" ? req.body.assertion : undefined
			if (!assertion) {
				res.status(400).json({
					error: "invalid_request",
					error_description: "Missing assertion",
				})
				return
			}

			const host = req.get("host") ?? "localhost"
			const audience = `https://${host}${tokenPath}`

			const { payload } = await jwtVerify(assertion, JWKS, {
				issuer,
				audience,
				algorithms: ["RS256"],
			})

			const result = await options.handleJwtGrant(payload, req)
			if (!result) return next()
			res.json(result)
		} catch (error) {
			console.error(error)
			res.status(400).json({ error: "invalid_grant" })
		}
	})

	return tokenRouter
}

export function mountIdentity(app: Application, options: IdentityHandler) {
	app.use(createIdentityTokenRouter(options))
}
