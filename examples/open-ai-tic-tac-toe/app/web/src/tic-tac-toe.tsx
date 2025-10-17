import { useTheme, useToolResponseMetadata, useDisplayMode, useMaxHeight, useCallTool, useRequestDisplayMode } from "@smithery/sdk/react"
import { useEffect, useRef, CSSProperties } from "react"
import confetti from "canvas-confetti"
import type { GameState } from "../../shared/types.js"

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
    transition: 'all 0.2s',
  }

  return (
    <button style={buttonStyle} onClick={onClick}>
      Expand
    </button>
  )
}

export default function TicTacToe() {
  const errorStyle: CSSProperties = {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    padding: '40px 20px',
    textAlign: 'center',
    color: '#6b7280',
  }

  if (!window.openai) {
    return (
      <div style={errorStyle}>
        <p>Please open this widget in a supporitng client</p>
      </div>
    )
  }

  const theme = useTheme()
  const displayMode = useDisplayMode()
  const maxHeight = useMaxHeight()
  const metadata = useToolResponseMetadata<{ gameState?: GameState }>()
  const requestDisplayMode = useRequestDisplayMode()
  
  const { call: makeMove } = useCallTool<{ position: number }>("make-move")
  const { call: startGame } = useCallTool("start-game")
  
  const gameState = metadata?.gameState ?? {
    board: Array(9).fill(null),
    currentPlayer: "X" as const,
    gameOver: false,
    winner: null,
  }

  const isFullscreen = displayMode === "fullscreen"
  const isDark = theme === "dark"
  const previousWinnerRef = useRef<string | null>(null)

  useEffect(() => {
    if (gameState.gameOver && gameState.winner && gameState.winner !== "draw" && previousWinnerRef.current !== gameState.winner) {
      previousWinnerRef.current = gameState.winner
      
      const duration = 3000
      const animationEnd = Date.now() + duration
      const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 }

      const interval = setInterval(() => {
        const timeLeft = animationEnd - Date.now()

        if (timeLeft <= 0) {
          clearInterval(interval)
          return
        }

        const particleCount = 50 * (timeLeft / duration)
        
        confetti({
          ...defaults,
          particleCount,
          origin: { x: Math.random() * 0.4 + 0.3, y: Math.random() - 0.2 }
        })
      }, 250)

      return () => clearInterval(interval)
    }
    
    if (!gameState.gameOver) {
      previousWinnerRef.current = null
    }
  }, [gameState.gameOver, gameState.winner])

  const handleCellClick = async (index: number) => {
    if (!gameState.gameOver && gameState.board[index] === null) {
      await makeMove({ position: index })
    }
  }

  const handleNewGame = async () => {
    await startGame({})
  }

  const getStatusText = () => {
    if (gameState.gameOver) {
      if (gameState.winner === "draw") return "Draw!"
      return `${gameState.winner} Wins!`
    }
    return `${gameState.currentPlayer}'s Turn`
  }

  const containerStyle: CSSProperties = {
    position: 'relative',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "SF Pro Display", sans-serif',
    padding: isFullscreen ? '60px 20px' : '40px 20px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    overflow: 'hidden',
    minHeight: isFullscreen ? undefined : 500,
    borderRadius: isFullscreen ? 0 : 16,
    border: isFullscreen ? 'none' : isDark ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid rgba(0, 0, 0, 0.1)',
    backgroundColor: isDark ? '#0d0d0d' : '#fafafa',
    color: isDark ? '#e5e5e5' : '#1f2937',
    height: isFullscreen ? (maxHeight ?? "100vh") : undefined,
    maxHeight: maxHeight ?? "100vh",
  }

  const titleStyle: CSSProperties = {
    textAlign: 'center',
    marginBottom: 10,
    fontWeight: 600,
    letterSpacing: '-0.02em',
    fontSize: isFullscreen ? 32 : 24,
    transition: 'font-size 0.2s ease',
  }

  const statusStyle: CSSProperties = {
    textAlign: 'center',
    fontSize: isFullscreen ? 22 : 18,
    marginBottom: isFullscreen ? 30 : 20,
    fontWeight: 'bold',
    transition: 'font-size 0.2s ease',
  }

  const boardStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(3, ${isFullscreen ? 120 : 100}px)`,
    gap: isFullscreen ? 12 : 10,
    marginBottom: isFullscreen ? 30 : 20,
    transition: 'all 0.2s ease',
  }

  const buttonStyle: CSSProperties = {
    width: 320,
    padding: 12,
    fontSize: 16,
    fontWeight: 600,
    color: '#fff',
    backgroundColor: '#007AFF',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    transition: 'all 0.2s',
  }

  return (
    <div style={containerStyle}>
      {!isFullscreen && (
        <ExpandButton onClick={() => requestDisplayMode('fullscreen')} />
      )}

      <h1 style={titleStyle}>Tic-Tac-Toe</h1>
      
      <div style={statusStyle}>
        {getStatusText()}
      </div>
      
      <div style={boardStyle}>
        {gameState.board.map((cell, index) => {
          const isClickable = !gameState.gameOver && cell === null
          
          const cellStyle: CSSProperties = {
            width: isFullscreen ? 120 : 100,
            height: isFullscreen ? 120 : 100,
            fontSize: isFullscreen ? 40 : 32,
            fontWeight: 'bold',
            borderRadius: 6,
            transition: 'all 0.2s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: isClickable ? 'pointer' : 'not-allowed',
            backgroundColor: isDark ? '#1c1c1c' : '#ffffff',
            border: `2px solid ${isDark ? '#2d2d2d' : '#e5e7eb'}`,
            color: isDark ? '#e5e5e5' : '#1f2937',
            opacity: isClickable ? 1 : 0.6,
          }

          return (
            <button
              key={index}
              style={cellStyle}
              onClick={() => handleCellClick(index)}
              disabled={!isClickable}
            >
              {cell}
            </button>
          )
        })}
      </div>
      
      <button style={buttonStyle} onClick={handleNewGame}>
        {gameState.gameOver ? "New Game" : "Reset"}
      </button>
    </div>
  )
}
