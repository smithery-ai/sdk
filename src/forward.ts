import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js"
import { JSONRPCMessage } from "@modelcontextprotocol/sdk/types"

/**
 * A transport that just forwards messages to another transport
 */
export class ForwardTransport implements Transport {
  private started = false
  private isClosed = false
  private other: ForwardTransport | null = null

  onclose?: () => void
  onerror?: (error: Error) => void
  onmessage?: (message: JSONRPCMessage) => void

  /**
   * Sets the other transport to forward messages to
   */
  bind(other: ForwardTransport) {
    this.other = other
  }

  async start() {
    if (this.started) {
      throw new Error(
        "StdioServerTransport already started! If using Server class, note that connect() calls start() automatically."
      )
    }
    if (!this.other) throw new Error("Client not set.")
    this.started = true
  }

  async close() {
    if (this.isClosed) return

    this.isClosed = true
    this.onclose?.()
    await this.other?.close()
  }

  async send(message: JSONRPCMessage) {
    if (!this.other) throw new Error("Client not set.")
    this.other.onmessage?.(message)
  }
}
