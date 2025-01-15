export function createSmitheryUrl(baseUrl: string, config: object) {
	const url = new URL(baseUrl)
	const param =
		typeof window !== "undefined"
			? btoa(JSON.stringify(config))
			: Buffer.from(JSON.stringify(config)).toString("base64")
	url.searchParams.set("config", param)
	return url
}
