import { createRoot } from 'react-dom/client'
import Greeter from './greeter.js'

const rootElement = document.getElementById('greeter-root')
if (rootElement) {
  const root = createRoot(rootElement)
  root.render(<Greeter />)
}

