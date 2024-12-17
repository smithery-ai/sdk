import type { z } from "zod"

export type ToolParameters = z.ZodTypeAny

export interface Tool<Params extends ToolParameters = ToolParameters> {
	name: string
	description?: string
	parameters?: Params
	execute: (args: z.infer<Params>) => Promise<any>
}

export interface Resource {
	uri: string
	name: string
	description?: string
	mimeType?: string
	load: () => Promise<{ text: string } | { blob: string }>
}

export type PromptArgument = Readonly<{
	name: string
	description?: string
	required?: boolean
}>

type ArgumentsToObject<T extends PromptArgument[]> = {
	[K in T[number]["name"]]: Extract<
		T[number],
		{ name: K }
	>["required"] extends true
		? string
		: string | undefined
}

export interface Prompt<
	Arguments extends PromptArgument[] = PromptArgument[],
	Args = ArgumentsToObject<Arguments>,
> {
	name: string
	description?: string
	arguments?: Arguments
	load: (args: Args) => Promise<string>
}
