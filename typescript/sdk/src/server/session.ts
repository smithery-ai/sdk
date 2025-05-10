import type { Transport } from "@modelcontextprotocol/sdk/shared/transport.js"

export interface SessionStore<T extends Transport> {
	/** return existing transport (or `undefined`) */
	get(id: string): T | undefined
	/** insert / update */
	set(id: string, t: T): void
	/** optional - explicit eviction */
	delete?(id: string): void
}

/**
 * Minimal Map‑based LRU implementation that fulfils {@link SessionStore}.
 * Keeps at most `max` transports; upon insert, the least‑recently‑used entry
 * (oldest insertion order) is removed and the evicted transport is closed.
 *
 * @param max  maximum number of sessions to retain (default = 1000)
 */
export const createLRUStore = <T extends Transport>(
	max = 1000,
): SessionStore<T> => {
	// ECMA‑262 §23.1.3.13 - the order of keys in a Map object is the order of insertion; operations that remove a key drop it from that order, and set appends when the key is new or has just been removed.
	const cache = new Map<string, T>()

	return {
		get: (id) => {
			const t = cache.get(id)
			if (!t) return undefined
			// refresh position
			cache.delete(id)
			cache.set(id, t)
			return t
		},

		set: (id, transport) => {
			if (cache.has(id)) {
				// key already present - refresh position
				cache.delete(id)
			} else if (cache.size >= max) {
				// evict oldest entry (first in insertion order)
				const [lruId, lruTransport] = cache.entries().next().value as [
					string,
					T,
				]
				lruTransport.close?.()
				cache.delete(lruId)
			}
			cache.set(id, transport)
		},

		delete: (id) => cache.delete(id),
	}
}
