export function createSmitheryUrl(baseUrl: string, config?: object, apiKey?: string) {
	const url = new URL(baseUrl)
	if (config) {
		const param =
			typeof window !== "undefined"
				? btoa(JSON.stringify(config))
				: Buffer.from(JSON.stringify(config)).toString("base64")
		url.searchParams.set("config", param)
	}
	if (apiKey) {
		url.searchParams.set("api_key", apiKey)
	}
	return url
}
