import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { widget } from "@smithery/sdk"
import type { GameState } from "./types.js"

let gameState: GameState = {
  board: Array(9).fill(null),
  currentPlayer: "X",
  gameOver: false,
  winner: null,
}

const checkWinner = (board: (string | null)[]): "X" | "O" | null => {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ]

  for (const [a, b, c] of lines) {
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return board[a] as "X" | "O"
    }
  }

  return null
}

const isBoardFull = (board: (string | null)[]): boolean => 
  board.every(cell => cell !== null)

export default function createServer() {
  const server = new McpServer({
    name: "Tic-Tac-Toe Game",
    version: "1.0.0",
  })

  const ticTacToeWidget = widget.resource<GameState>({
    name: "tic-tac-toe",
    description: "An interactive tic-tac-toe game board. Users can click cells to make moves, and the game tracks X and O turns automatically.",
    prefersBorder: true,
  })

  server.registerResource(
    ticTacToeWidget.name,
    ticTacToeWidget.uri,
    {},
    ticTacToeWidget.handler
  )

  server.registerTool(
    "start-game",
    {
      title: "Start New Game",
      description: "Start a new tic-tac-toe game",
      inputSchema: {},
      _meta: ticTacToeWidget.toolConfig({
        invoking: "Starting new game...",
        invoked: "Game started",
      }),
    },
    async () => {
      gameState = {
        board: Array(9).fill(null),
        currentPlayer: "X",
        gameOver: false,
        winner: null,
      }

      return ticTacToeWidget.response({
        structuredData: gameState,
        message: "Game started. The interactive board is displayed above - do not describe or explain the board, just let the user play.",
        meta: {
          gameState,
          lastSyncedAt: new Date().toISOString(),
        },
      })
    }
  )

  server.registerTool(
    "make-move",
    {
      title: "Make Move",
      description: "Make a move in the tic-tac-toe game",
      inputSchema: {
        position: z.number().min(0).max(8).describe("Board position (0-8)"),
      },
      _meta: ticTacToeWidget.toolConfig({
        invoking: "Making move...",
        invoked: "Move completed",
        widgetAccessible: true,
      }),
    },
    async (args) => {
      const { position } = args

      if (gameState.gameOver) {
        return widget.error("Game is over. Start a new game to continue.")
      }

      if (gameState.board[position] !== null) {
        return widget.error(`Position ${position} is already occupied.`)
      }

      gameState.board[position] = gameState.currentPlayer

      const winner = checkWinner(gameState.board)
      if (winner) {
        gameState.winner = winner
        gameState.gameOver = true

        return ticTacToeWidget.response({
          structuredData: gameState,
          message: `${winner} wins!`,
          meta: {
            gameState,
            lastSyncedAt: new Date().toISOString(),
          },
        })
      }

      if (isBoardFull(gameState.board)) {
        gameState.winner = "draw"
        gameState.gameOver = true

        return ticTacToeWidget.response({
          structuredData: gameState,
          message: "It's a draw! The game is over and the user can see the final board in the widget.",
          meta: {
            gameState,
            lastSyncedAt: new Date().toISOString(),
          },
        })
      }

      gameState.currentPlayer = gameState.currentPlayer === "X" ? "O" : "X"

      return ticTacToeWidget.response({
        structuredData: gameState,
        message: `Move made. The user can see the updated board in the widget. It's now ${gameState.currentPlayer}'s turn.`,
        meta: {
          gameState,
          lastSyncedAt: new Date().toISOString(),
        },
      })
    }
  )

  server.registerTool(
    "get-game-state",
    {
      title: "Get Game State",
      description: "Get the current state of the tic-tac-toe game",
      inputSchema: {},
      _meta: ticTacToeWidget.toolConfig({
        invoking: "Getting game state...",
        invoked: "Retrieved game state",
      }),
    },
    async () => {
      return ticTacToeWidget.response({
        structuredData: gameState,
        message: `The user can see the board in the widget. ${
          gameState.gameOver
            ? `Game is over: ${gameState.winner === "draw" ? "Draw" : `${gameState.winner} wins`}.`
            : `Game in progress, ${gameState.currentPlayer}'s turn.`
        }`,
        meta: {
          gameState,
          lastSyncedAt: new Date().toISOString(),
        },
      })
    }
  )

  return server.server
}

