import { useTheme, useToolResponseMetadata, useDisplayMode, useMaxHeight, useCallTool } from "@smithery/sdk/react"
import { useEffect, useRef } from "react"
import confetti from "canvas-confetti"
import type { GameState } from "../../shared/types.js"
import "./tic-tac-toe.css"

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

export default function TicTacToe() {
  if (!window.openai) {
    return (
      <div className="ttt-error">
        <p>Please open this widget in ChatGPT</p>
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

  const containerClasses = [
    'ttt-container',
    isFullscreen ? 'fullscreen' : 'inline',
    isDark ? 'dark' : 'light'
  ].join(' ')

  const titleClasses = [
    'ttt-title',
    isFullscreen ? 'fullscreen' : 'inline'
  ].join(' ')

  const statusClasses = [
    'ttt-status',
    isFullscreen ? 'fullscreen' : ''
  ].filter(Boolean).join(' ')

  const boardClasses = [
    'ttt-board',
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

      <h1 className={titleClasses}>Tic-Tac-Toe</h1>
      
      <div className={statusClasses}>
        {getStatusText()}
      </div>
      
      <div className={boardClasses}>
        {gameState.board.map((cell, index) => {
          const isClickable = !gameState.gameOver && cell === null
          const cellClasses = [
            'ttt-cell',
            isFullscreen ? 'fullscreen' : '',
            isDark ? 'dark' : 'light',
            isClickable ? 'clickable' : 'disabled'
          ].filter(Boolean).join(' ')

          return (
            <button
              key={index}
              className={cellClasses}
              onClick={() => handleCellClick(index)}
              disabled={!isClickable}
            >
              {cell}
            </button>
          )
        })}
      </div>
      
      <button className="ttt-button" onClick={handleNewGame}>
        {gameState.gameOver ? "New Game" : "Reset"}
      </button>
    </div>
  )
}
