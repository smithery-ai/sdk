/**
 * Patches a function on an object
 * @param obj
 * @param key
 * @param patcher
 */

export function patch<
	// Overload 1: required function
	T extends {
		[P in K]: (...args: any[]) => any
	},
	K extends keyof T & string,
>(obj: T, key: K, patcher: (fn: T[K]) => T[K]): void

export function patch<
	// Overload 2: optional function
	T extends {
		[P in K]?: (...args: any[]) => any
	},
	K extends keyof T & string,
>(obj: T, key: K, patcher: (fn?: T[K]) => T[K]): void

// Unified implementation (not type-checked by callers)
export function patch(obj: any, key: string, patcher: any): void {
	// If the property is actually a function, bind it; otherwise undefined
	const original =
		typeof obj[key] === "function" ? obj[key].bind(obj) : undefined
	obj[key] = patcher(original)
}
