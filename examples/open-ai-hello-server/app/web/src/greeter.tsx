import React from "react"
import { useToolOutput, useTheme } from "@smithery/sdk/react"
import type { GreeterState } from "./types"

export default function Greeter() {
  const { structuredContent: state } = useToolOutput<GreeterState>()
  const theme = useTheme()

  if (!state) {
    return (
      <div
        style={{
          fontFamily: "system-ui, sans-serif",
          padding: "32px",
          textAlign: "center",
          color: theme === "dark" ? "#e5e5e5" : "#171717",
        }}
      >
        Loading...
      </div>
    )
  }

  return (
    <div
      style={{
        fontFamily: "system-ui, sans-serif",
        padding: "32px",
        textAlign: "center",
        backgroundColor: theme === "dark" ? "#1a1a1a" : "#ffffff",
        color: theme === "dark" ? "#e5e5e5" : "#171717",
        borderRadius: "8px",
      }}
    >
      <h1
        style={{
          fontSize: "32px",
          fontWeight: "700",
          margin: "0 0 16px 0",
        }}
      >
        {state.greeting}
      </h1>

      <p
        style={{
          fontSize: "14px",
          color: theme === "dark" ? "#a3a3a3" : "#737373",
          margin: 0,
        }}
      >
        Greeted {state.name} at{" "}
        {new Date(state.timestamp).toLocaleTimeString()}
      </p>
    </div>
  )
}

