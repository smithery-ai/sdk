import { useTheme, useToolResponseMetadata, useDisplayMode, useMaxHeight, useCallTool } from "@smithery/sdk/react"
import { useEffect, useRef } from "react"
import confetti from "canvas-confetti"
import type { GameState } from "../../server/types.js"

export default function TicTacToe() {
  if (!window.openai) {
    return (
      <div style={{
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        padding: "40px 20px",
        textAlign: "center",
        color: "#6b7280"
      }}>
        <p>Please open this widget in ChatGPT</p>
      </div>
    )
  }

  const theme = useTheme()
  const displayMode = useDisplayMode()
  const maxHeight = useMaxHeight()
  const metadata = useToolResponseMetadata<{ gameState?: GameState }>()
  
  const { call: makeMove } = useCallTool<{ position: number }>("make-move")
  const { call: startGame } = useCallTool("start-game")
  
  const gameState = metadata?.gameState ?? {
    board: Array(9).fill(null),
    currentPlayer: "X" as const,
    gameOver: false,
    winner: null,
  }

  const isFullscreen = displayMode === "fullscreen"
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

  return (
    <div style={{
      ...styles.container,
      backgroundColor: theme === "dark" ? "#0d0d0d" : "#fafafa",
      color: theme === "dark" ? "#e5e5e5" : "#1f2937",
      minHeight: isFullscreen ? (maxHeight ?? "100vh") : "100vh",
      maxHeight: maxHeight ?? "100vh",
      padding: isFullscreen ? "40px 20px" : "20px",
    }}>
      <h1 style={{
        ...styles.title,
        fontSize: isFullscreen ? "28px" : "24px",
      }}>Tic-Tac-Toe</h1>
      <div style={{
        ...styles.status,
        color: theme === "dark" ? "#e5e5e5" : "#1f2937"
      }}>
        {getStatusText()}
      </div>
      <div style={{
        ...styles.board,
        gridTemplateColumns: isFullscreen ? "repeat(3, 120px)" : "repeat(3, 100px)",
        gap: isFullscreen ? "12px" : "10px",
      }}>
        {gameState.board.map((cell, index) => (
          <button
            key={index}
            style={{
              ...styles.cell,
              width: isFullscreen ? "120px" : "100px",
              height: isFullscreen ? "120px" : "100px",
              fontSize: isFullscreen ? "40px" : "32px",
              backgroundColor: theme === "dark" ? "#1c1c1c" : "#ffffff",
              border: `2px solid ${theme === "dark" ? "#2d2d2d" : "#e5e7eb"}`,
              color: theme === "dark" ? "#e5e5e5" : "#1f2937",
              cursor: !gameState.gameOver && cell === null ? "pointer" : "not-allowed",
              opacity: !gameState.gameOver && cell === null ? 1 : 0.6,
            }}
            onClick={() => handleCellClick(index)}
            disabled={gameState.gameOver || cell !== null}
          >
            {cell}
          </button>
        ))}
      </div>
      <button 
        style={{
          ...styles.button,
          backgroundColor: theme === "dark" ? "#007AFF" : "#007AFF",
        }}
        onClick={handleNewGame}
      >
        {gameState.gameOver ? "New Game" : "Reset"}
      </button>
    </div>
  )
}

const styles = {
  container: {
    padding: "20px",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', sans-serif",
    display: "flex" as const,
    flexDirection: "column" as const,
    alignItems: "center" as const,
    minHeight: "100vh",
  } as const,
  title: {
    textAlign: "center" as const,
    marginBottom: "10px",
    fontSize: "24px",
    fontWeight: 600 as const,
    letterSpacing: "-0.02em",
  },
  status: {
    textAlign: "center" as const,
    fontSize: "18px",
    marginBottom: "20px",
    fontWeight: "bold" as const,
  },
  board: {
    display: "grid" as const,
    gridTemplateColumns: "repeat(3, 100px)",
    gap: "10px",
    marginBottom: "20px",
  },
  cell: {
    width: "100px",
    height: "100px",
    fontSize: "32px",
    fontWeight: "bold" as const,
    borderRadius: "6px",
    transition: "all 0.2s",
    display: "flex" as const,
    alignItems: "center" as const,
    justifyContent: "center" as const,
  },
  button: {
    width: "320px",
    padding: "12px",
    fontSize: "16px",
    fontWeight: 600 as const,
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer" as const,
    transition: "all 0.2s",
  } as const,
}

