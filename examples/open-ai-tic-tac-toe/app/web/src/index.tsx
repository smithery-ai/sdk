import { createRoot } from 'react-dom/client'
import TicTacToe from './tic-tac-toe.js'

const rootElement = document.getElementById('tic-tac-toe-root')
if (rootElement) {
  const root = createRoot(rootElement)
  root.render(<TicTacToe />)
}

