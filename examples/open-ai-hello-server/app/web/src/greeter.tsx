import { useEffect } from "react"
import confetti from "canvas-confetti"
import { useToolOutput, useTheme, useDisplayMode, useMaxHeight } from "@smithery/sdk/react"
import type { GreeterState } from "../../server/types.js"
import "./greeter.css"

const CONFETTI_COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#ffd700']

function useRequestDisplayMode() {
  return (mode: 'fullscreen' | 'inline' | 'pip') => {
    return window.openai?.requestDisplayMode?.({ mode })
  }
}

function ExpandButton({ onClick }: { onClick: () => void }) {
  return (
    <button className="expand-button" onClick={onClick}>
      Expand
    </button>
  )
}

export default function Greeter() {
  const { structuredContent: state } = useToolOutput<GreeterState>()
  const theme = useTheme()
  const displayMode = useDisplayMode()
  const maxHeight = useMaxHeight()
  const requestDisplayMode = useRequestDisplayMode()

  const isFullscreen = displayMode === "fullscreen"
  const isDark = theme === "dark"

  useEffect(() => {
    if (state) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: CONFETTI_COLORS,
      })
    }
  }, [state?.timestamp])

  if (!state) {
    return (
      <div className={`greeter-loading ${isDark ? 'dark' : 'light'}`}>
        Loading...
      </div>
    )
  }

  const containerClasses = [
    'greeter-container',
    isFullscreen ? 'fullscreen' : 'inline',
    isDark ? 'dark' : 'light'
  ].join(' ')

  const headingClasses = [
    'greeter-heading',
    isFullscreen ? 'fullscreen' : 'inline',
    isDark ? 'dark' : 'light'
  ].join(' ')

  const emojiClasses = [
    'greeter-emoji',
    isFullscreen ? 'fullscreen' : ''
  ].filter(Boolean).join(' ')

  return (
    <div 
      className={containerClasses}
      style={{ 
        height: isFullscreen ? (maxHeight ?? "100vh") : undefined,
        maxHeight: maxHeight ?? "100vh" 
      }}
    >
      {!isFullscreen && (
        <ExpandButton onClick={() => requestDisplayMode('fullscreen')} />
      )}

      <h1 className={headingClasses}>
        {state.greeting}
        <span className={emojiClasses}>
          👋
        </span>
      </h1>
    </div>
  )
}

