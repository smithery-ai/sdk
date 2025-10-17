import { createRoot } from 'react-dom/client'
import CoffeeMap from './coffee-map.js'

const rootElement = document.getElementById('coffee-map-root')
if (rootElement) {
  const root = createRoot(rootElement)
  root.render(<CoffeeMap />)
}

