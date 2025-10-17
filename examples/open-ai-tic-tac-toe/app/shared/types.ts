export type CellValue = "X" | "O" | null

export interface GameState {
  board: CellValue[]
  currentPlayer: "X" | "O"
  gameOver: boolean
  winner: "X" | "O" | "draw" | null
}

