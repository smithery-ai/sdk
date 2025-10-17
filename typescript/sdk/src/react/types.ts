export type Theme = "light" | "dark"
export type DisplayMode = "inline" | "pip" | "fullscreen"

export interface DeviceType {
	type: "mobile" | "tablet" | "desktop" | "unknown"
}

export interface UserAgent {
	device: DeviceType
	capabilities: {
		hover: boolean
		touch: boolean
	}
}

export interface SafeAreaInsets {
	top: number
	bottom: number
	left: number
	right: number
}

export interface SafeArea {
	insets: SafeAreaInsets
}

export interface CallToolResponse {
	content?: Array<{ type: string; text: string }>
	structuredContent?: unknown
	_meta?: Record<string, unknown>
	isError?: boolean
}

export interface OpenAiGlobals {
	theme: Theme
	displayMode: DisplayMode
	userAgent: UserAgent
	locale: string

	maxHeight: number
	safeArea: SafeArea

	toolInput: Record<string, unknown>
	toolOutput: {
		content?: Array<{ type: string; text: string }>
		structuredContent?: unknown
	} | null
	toolResponseMetadata: Record<string, unknown> | null

	widgetState: Record<string, unknown> | null

	callTool: (
		name: string,
		args: Record<string, unknown>,
	) => Promise<CallToolResponse>
	sendFollowUpMessage: (args: { prompt: string }) => Promise<void>
	openExternal: (payload: { href: string }) => void
	requestDisplayMode: (args: {
		mode: DisplayMode
	}) => Promise<{ mode: DisplayMode }>
	setWidgetState: (state: Record<string, unknown>) => Promise<void>
}

declare global {
	interface Window {
		openai?: OpenAiGlobals
	}
}
