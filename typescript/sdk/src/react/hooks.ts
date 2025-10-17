import {
	useSyncExternalStore,
	useCallback,
	useState,
	useEffect,
	type SetStateAction,
} from "react"
import type { OpenAiGlobals } from "./types.js"

const SET_GLOBALS_EVENT_TYPE = "openai:set_globals"

function getOpenAiGlobal<K extends keyof OpenAiGlobals>(
	key: K,
): OpenAiGlobals[K] | undefined {
	if (!window.openai) return undefined
	return window.openai[key]
}

function subscribeToOpenAi(callback: () => void) {
	const handler = () => callback()
	window.addEventListener(SET_GLOBALS_EVENT_TYPE, handler)
	return () => window.removeEventListener(SET_GLOBALS_EVENT_TYPE, handler)
}

export function useOpenAiGlobal<K extends keyof OpenAiGlobals>(
	key: K,
): OpenAiGlobals[K] | undefined {
	return useSyncExternalStore(
		subscribeToOpenAi,
		() => getOpenAiGlobal(key),
		() => undefined,
	)
}

export function useTheme() {
	return useOpenAiGlobal("theme") ?? "dark"
}

export function useDisplayMode() {
	return useOpenAiGlobal("displayMode") ?? "inline"
}

export function useUserAgent() {
	return useOpenAiGlobal("userAgent")
}

export function useMaxHeight() {
	return useOpenAiGlobal("maxHeight")
}

export function useSafeArea() {
	return useOpenAiGlobal("safeArea")
}

export function useLocale() {
	return useOpenAiGlobal("locale") ?? "en"
}

export function useToolInput<T = Record<string, unknown>>() {
	return useOpenAiGlobal("toolInput") as T | undefined
}

export function useToolOutput<T = unknown>() {
	const output = useOpenAiGlobal("toolOutput")
	return {
		content: output?.content ?? [],
		structuredContent: output?.structuredContent as T | undefined,
	}
}

export function useToolResponseMetadata<T = Record<string, unknown>>() {
	return useOpenAiGlobal("toolResponseMetadata") as T | undefined
}

export function useCallTool<TArgs = Record<string, unknown>, TResult = unknown>(
	toolName: string,
) {
	const [isPending, setIsPending] = useState(false)
	const [error, setError] = useState<Error | null>(null)
	const [data, setData] = useState<TResult | null>(null)

	const callTool = useOpenAiGlobal("callTool")

	const call = useCallback(
		async (args: TArgs) => {
			if (!callTool) {
				setError(new Error("callTool not available"))
				return
			}

			setIsPending(true)
			setError(null)

			try {
				const result = await callTool(toolName, args as Record<string, unknown>)

				if (result.isError) {
					throw new Error(result.content?.[0]?.text ?? "Unknown error")
				}

				setData(
					(result._meta?.gameState ??
						result.structuredContent ??
						null) as TResult,
				)
			} catch (err) {
				setError(err instanceof Error ? err : new Error(String(err)))
			} finally {
				setIsPending(false)
			}
		},
		[callTool, toolName],
	)

	return { call, isPending, error, data }
}

export function useSendFollowUp() {
	const [isPending, setIsPending] = useState(false)
	const [error, setError] = useState<Error | null>(null)

	const sendFollowUpMessage = useOpenAiGlobal("sendFollowUpMessage")

	const send = useCallback(
		async (prompt: string) => {
			if (!sendFollowUpMessage) {
				setError(new Error("sendFollowUpMessage not available"))
				return
			}

			setIsPending(true)
			setError(null)

			try {
				await sendFollowUpMessage({ prompt })
			} catch (err) {
				setError(err instanceof Error ? err : new Error(String(err)))
			} finally {
				setIsPending(false)
			}
		},
		[sendFollowUpMessage],
	)

	return { send, isPending, error }
}

export function useRequestDisplayMode() {
	const requestDisplayMode = useOpenAiGlobal("requestDisplayMode")

	const request = useCallback(
		async (mode: "inline" | "pip" | "fullscreen") => {
			if (!requestDisplayMode) {
				return
			}
			await requestDisplayMode({ mode })
		},
		[requestDisplayMode],
	)

	return request
}

export function useWidgetState<T extends Record<string, unknown>>(
	defaultState: T | (() => T),
): readonly [T, (state: SetStateAction<T>) => void]
export function useWidgetState<T extends Record<string, unknown>>(
	defaultState?: T | (() => T | null) | null,
): readonly [T | null, (state: SetStateAction<T | null>) => void]
export function useWidgetState<T extends Record<string, unknown>>(
	defaultState?: T | (() => T | null) | null,
): readonly [T | null, (state: SetStateAction<T | null>) => void] {
	const widgetStateFromWindow = useOpenAiGlobal("widgetState") as T | null

	const [widgetState, _setWidgetState] = useState<T | null>(() => {
		if (widgetStateFromWindow != null) {
			return widgetStateFromWindow
		}
		return typeof defaultState === "function"
			? defaultState()
			: (defaultState ?? null)
	})

	useEffect(() => {
		if (widgetStateFromWindow != null) {
			_setWidgetState(widgetStateFromWindow)
		}
	}, [widgetStateFromWindow])

	const setWidgetState = useCallback((state: SetStateAction<T | null>) => {
		_setWidgetState((prevState: T | null) => {
			const newState = typeof state === "function" ? state(prevState) : state
			if (newState != null && window.openai?.setWidgetState) {
				window.openai.setWidgetState(newState)
			}
			return newState
		})
	}, [])

	return [widgetState, setWidgetState] as const
}
