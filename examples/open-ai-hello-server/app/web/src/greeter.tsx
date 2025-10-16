import { useEffect } from "react"
import confetti from "canvas-confetti"
import { useToolOutput, useTheme } from "@smithery/sdk/react"
import type { GreeterState } from "../../server/types.js"

export default function Greeter() {
  const { structuredContent: state } = useToolOutput<GreeterState>()
  const theme = useTheme()

  useEffect(() => {
    if (state) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#ffd700']
      })
    }
  }, [state?.timestamp])

  if (!state) {
    return (
      <div
        style={{
          fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
          padding: "48px",
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
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        padding: "80px 32px",
        textAlign: "center",
        backgroundColor: theme === "dark" ? "#0d0d0d" : "#fafafa",
        minHeight: "400px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <h1
        style={{
          fontSize: "32px",
          fontWeight: "600",
          margin: 0,
          color: theme === "dark" ? "#ffffff" : "#1f2937",
          letterSpacing: "-0.02em",
          display: "flex",
          alignItems: "center",
          gap: "12px",
        }}
      >
        {state.greeting}
        <span
          style={{
            display: "inline-block",
            animation: "wave 1.2s ease-in-out",
            transformOrigin: "70% 70%",
          }}
        >
          👋
        </span>
      </h1>

      <style>
        {`
          @keyframes wave {
            0% { transform: rotate(0deg); }
            10% { transform: rotate(14deg); }
            20% { transform: rotate(-8deg); }
            30% { transform: rotate(14deg); }
            40% { transform: rotate(-4deg); }
            50% { transform: rotate(10deg); }
            60% { transform: rotate(0deg); }
            100% { transform: rotate(0deg); }
          }
        `}
      </style>
    </div>
  )
}

