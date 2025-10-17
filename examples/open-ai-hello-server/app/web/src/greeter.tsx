import { useEffect, CSSProperties } from "react"
import confetti from "canvas-confetti"
import { useToolOutput, useTheme, useDisplayMode, useMaxHeight, useRequestDisplayMode } from "@smithery/sdk/react"
import type { GreeterState } from "../../server/types.js"

const CONFETTI_COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#ffd700']

function ExpandButton({ onClick }: { onClick: () => void }) {
  const buttonStyle: CSSProperties = {
    position: 'absolute',
    top: 12,
    right: 12,
    zIndex: 30,
    background: 'white',
    border: 'none',
    borderRadius: 8,
    padding: '8px 12px',
    cursor: 'pointer',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    fontSize: 14,
    fontWeight: 500,
  }

  return (
    <button style={buttonStyle} onClick={onClick}>
      Expand
    </button>
  )
}

function Greeter() {
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

  const loadingStyle: CSSProperties = {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    padding: 48,
    textAlign: 'center',
    color: isDark ? '#e5e5e5' : '#171717',
  }

  if (!state) {
    return <div style={loadingStyle}>Loading...</div>
  }

  const containerStyle: CSSProperties = {
    position: 'relative',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    padding: '80px 32px',
    textAlign: 'center',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    height: isFullscreen ? (maxHeight ?? "100vh") : 400,
    maxHeight: maxHeight ?? "100vh",
    borderRadius: isFullscreen ? 0 : 16,
    border: isFullscreen ? 'none' : isDark ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid rgba(0, 0, 0, 0.1)',
    backgroundColor: isDark ? '#0d0d0d' : '#fafafa',
    color: isDark ? '#ffffff' : '#1f2937',
  }

  const headingStyle: CSSProperties = {
    fontWeight: 600,
    margin: 0,
    letterSpacing: '-0.02em',
    display: 'flex',
    alignItems: 'center',
    fontSize: isFullscreen ? 48 : 32,
    gap: isFullscreen ? 16 : 12,
    transition: 'font-size 0.2s ease',
  }

  const emojiStyle: CSSProperties = {
    display: 'inline-block',
    animation: 'wave 1.2s ease-in-out',
    transformOrigin: '70% 70%',
    fontSize: isFullscreen ? 56 : 'inherit',
    transition: 'font-size 0.2s ease',
  }

  return (
    <>
      <style>{`
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
      `}</style>
      <div style={containerStyle}>
        {!isFullscreen && (
          <ExpandButton onClick={() => requestDisplayMode('fullscreen')} />
        )}

        <h1 style={headingStyle}>
          {state.greeting}
          <span style={emojiStyle}>👋</span>
        </h1>
      </div>
    </>
  )
}

// Export as Component for the build script to mount
export default Greeter
