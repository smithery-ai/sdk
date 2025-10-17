export {
	useOpenAiGlobal,
	useTheme,
	useDisplayMode,
	useUserAgent,
	useMaxHeight,
	useSafeArea,
	useLocale,
	useToolInput,
	useToolOutput,
	useToolResponseMetadata,
	useWidgetState,
	useCallTool,
	useSendFollowUp,
	useRequestDisplayMode,
} from "./hooks.js"

export type {
	Theme,
	DisplayMode,
	DeviceType,
	UserAgent,
	SafeAreaInsets,
	SafeArea,
	CallToolResponse,
	OpenAiGlobals,
} from "./types.js"

export { ErrorBoundary } from "./ErrorBoundary.js"
