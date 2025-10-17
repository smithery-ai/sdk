# AGENTS.md - Building ChatGPT Apps with Smithery

Reference guide for AI agents building interactive ChatGPT apps using Model Context Protocol (MCP) and Smithery SDK.

---

## Overview

**What are ChatGPT apps?** Interactive React components that render tool results in ChatGPT, displayed in sandboxed iframes with bidirectional communication.

**Architecture:**
```
[ChatGPT] <-> [Sandboxed Iframe] <-> [MCP Server]
              window.openai API      MCP Protocol
```

**Key capabilities:**
- Render rich UIs from tool results
- Call tools back to server from app
- Persist UI state across sessions
- Theme-aware (light/dark)
- Display modes (inline/pip/fullscreen)

---

## Project Structure

```
app/
├── server/
│   └── index.ts       # MCP server with widget resource
├── shared/
│   └── types.ts       # Shared type definitions
└── web/
    └── src/
        ├── index.tsx      # React entry point
        └── {app-name}.tsx # App component
smithery.yaml          # Configuration (runtime + type)
package.json
```

**smithery.yaml:**
```yaml
runtime: typescript
type: widget
```

**Key conventions:**
- `runtime: typescript` - Specifies TypeScript runtime
- `type: widget` - Tells CLI to bundle both server and client
- App components export as default
- Types defined in `app/shared/types.ts` - imported by both server and client
- CLI auto-generates HTML resource from bundled JS

---

## Server Side (MCP)

### 1. Create Widget Resource

Use `widget.resource<T>()` to define a widget resource:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { widget } from "@smithery/sdk"
import type { GreeterState } from "../shared/types.js"

export default function createServer() {
  const server = new McpServer({
    name: "Hello Widget",
    version: "1.0.0",
  })

  // Define widget resource
  const greeterWidget = widget.resource<GreeterState>({
    name: "greeter",  // Auto-generates uri: ui://widget/greeter.html
    description: "A simple greeting app",
  })

  // Register resource
  server.registerResource(
    greeterWidget.name,
    greeterWidget.uri,
    {},
    greeterWidget.handler
  )

  return server.server
}
```

**What it does:**
- Auto-generates URI: `ui://widget/{name}.html`
- Auto-generates HTML with `<div id="{name}-root"></div>`
- Loads bundled JS from `.smithery/{name}.js`
- Handles all widget metadata

### 2. Register Tool That Uses Widget

```typescript
import { z } from "zod"

server.registerTool(
  "say-hello",
  {
    title: "Say Hello",
    description: "Greet someone by name",
    inputSchema: {
      name: z.string().min(1).describe("Name of person to greet"),
    },
    _meta: greeterWidget.toolConfig({
      invoking: "Preparing greeting...",
      invoked: "Greeting ready!",
    }),
  },
  async (args) => {
    const { name } = args

    const structuredData: GreeterState = {
      name,
      greeting: `Hello, ${name}!`,
      timestamp: new Date().toISOString(),
    }

    return greeterWidget.response({
      structuredData,  // Data for both model and app
      message: `Said hello to ${name}`,  // Text for model conversation
    })
  }
)
```

**Key metadata from toolConfig():**
- `openai/outputTemplate` - App URI
- `openai/widgetAccessible: true` - App can call this tool
- `openai/toolInvocation/invoking` - Status text while executing
- `openai/toolInvocation/invoked` - Status text after completion

### 3. Tool Response Structure

Three fields control data distribution:

```typescript
return {
  structuredContent: {
    // Visible to BOTH model and app
    // Model can reason about this data
    // Keep concise - only what model needs
  },
  content: [
    // Text for model conversation only
    { type: "text", text: "Description for chat" }
  ],
  _meta: {
    // Invisible to model, visible to app only
    // Use for: full datasets, UI config, internal IDs
  }
}
```

**Design pattern:**
- `structuredContent`: Summary for model reasoning (e.g., "5 tasks in 3 columns")
- `content`: Natural language for conversation (e.g., "Here's your kanban board")
- `_meta`: Full datasets for app UI (e.g., complete task objects with descriptions)

---

## Client Side (React)

### 1. App Component Structure

```typescript
import { useToolOutput, useTheme, useDisplayMode } from "@smithery/sdk/react"
import type { GreeterState } from "../../../shared/types.js"

export default function Greeter() {
  const { structuredContent: state } = useToolOutput<GreeterState>()
  const theme = useTheme()
  const displayMode = useDisplayMode()

  if (!state) {
    return <div>Loading...</div>
  }

  return (
    <div className={`greeter ${theme}`}>
      <h1>{state.greeting}</h1>
      <p>Greeted at: {state.timestamp}</p>
    </div>
  )
}
```

**Key hooks:**
- `useToolOutput<T>()` - Access tool response data
- `useTheme()` - "light" | "dark" (default: "dark")
- `useDisplayMode()` - "inline" | "pip" | "fullscreen" (default: "inline")

### 2. Calling Tools from App

```typescript
import { useCallTool } from "@smithery/sdk/react"

export default function InteractiveApp() {
  const { structuredContent: gameState } = useToolOutput<GameState>()
  const makeMove = useCallTool<{ position: number }, GameState>("make-move")

  const handleMove = async (pos: number) => {
    await makeMove.call({ position: pos })
  }

  return (
    <div>
      <button
        onClick={() => handleMove(0)}
        disabled={makeMove.isPending}
      >
        {makeMove.isPending ? "Moving..." : "Make Move"}
      </button>
      {makeMove.error && <div>{makeMove.error.message}</div>}
    </div>
  )
}
```

**useCallTool<TArgs, TResult>(toolName) returns:**
- `call(args)` - Execute tool
- `isPending` - Loading state
- `error` - Error object or null
- `data` - Result data or null

**Important:** Tool must have `openai/widgetAccessible: true` in its `_meta`.

### 3. Persistent App State

```typescript
import { useWidgetState } from "@smithery/sdk/react"

interface UIState {
  selectedId: string | null
  expandedSections: string[]
}

export default function StatefulApp() {
  const [uiState, setUiState] = useWidgetState<UIState>({
    selectedId: null,
    expandedSections: [],
  })

  const toggle = (id: string) => {
    setUiState(prev => ({
      ...prev,
      expandedSections: prev.expandedSections.includes(id)
        ? prev.expandedSections.filter(x => x !== id)
        : [...prev.expandedSections, id]
    }))
  }

  return <div>{/* Use uiState */}</div>
}
```

**Key behavior:**
- State persists across tool calls and panel close/reopen
- State IS visible to the model (helps with context)
- Keep under 4k tokens
- Good for: user selections, filters, UI preferences

### 4. Other Useful Hooks

```typescript
import {
  useToolInput,           // Tool arguments
  useToolResponseMetadata,  // _meta field from response
  useMaxHeight,           // Max height in pixels
  useSafeArea,           // Safe area insets
  useUserAgent,          // Device capabilities
  useLocale,             // User locale
} from "@smithery/sdk/react"

const args = useToolInput<{ name: string }>()
const metadata = useToolResponseMetadata<{ shops?: Shop[] }>()
const maxHeight = useMaxHeight()
const safeArea = useSafeArea()
const userAgent = useUserAgent()
const locale = useLocale()
```

---

## Essential Patterns

### Pattern 1: Responsive Layout

```typescript
const displayMode = useDisplayMode()
const maxHeight = useMaxHeight()
const theme = useTheme()

const containerStyle = {
  height: displayMode === "fullscreen" ? (maxHeight ?? "100vh") : 400,
  borderRadius: displayMode === "fullscreen" ? 0 : 16,
  backgroundColor: theme === "dark" ? "#0d0d0d" : "#fafafa",
}

return <div style={containerStyle}>{/* content */}</div>
```

### Pattern 2: Expand to Fullscreen

```typescript
import { useDisplayMode, useRequestDisplayMode } from "@smithery/sdk/react"

export default function Widget() {
  const displayMode = useDisplayMode()
  const requestDisplayMode = useRequestDisplayMode()

  return (
    <div>
      {displayMode !== "fullscreen" && (
        <button onClick={() => requestDisplayMode("fullscreen")}>
          Expand
        </button>
      )}
    </div>
  )
}
```

### Pattern 3: Loading & Error States

```typescript
const { structuredContent: state } = useToolOutput<GameState>()
const makeMove = useCallTool<{ position: number }, GameState>("make-move")

if (!state) {
  return <div>Loading game...</div>
}

return (
  <div>
    {/* Game UI */}
    {makeMove.isPending && <div>Processing move...</div>}
    {makeMove.error && <div>Error: {makeMove.error.message}</div>}
  </div>
)
```

### Pattern 4: Send Follow-Up Message

```typescript
import { useSendFollowUp } from "@smithery/sdk/react"

export default function ActionPanel() {
  const followUp = useSendFollowUp()

  const handleAsk = async () => {
    await followUp.send("Create an itinerary for these items")
  }

  return (
    <button onClick={handleAsk} disabled={followUp.isPending}>
      {followUp.isPending ? "Asking..." : "Create Itinerary"}
    </button>
  )
}
```

---

## Type Safety

### Shared Types Pattern

```typescript
// app/shared/types.ts
export interface GreeterState extends Record<string, unknown> {
  name: string
  greeting: string
  timestamp: string
}

// app/server/index.ts
import type { GreeterState } from "../shared/types.js"

  const greeterWidget = widget.resource<GreeterState>({
    name: "greeter",
    description: "A simple greeting app",
  })

// app/web/src/greeter.tsx
import type { GreeterState } from "../../../shared/types.js"

const { structuredContent: state } = useToolOutput<GreeterState>()
```

**Best practice:** Define types in `app/shared/types.ts`, import from both server and client.

---

## Development Workflow

### 1. Local Development

```bash
# Install dependencies
npm install

# Start dev server (runs on port 3000 by default)
npm run dev

# Test in MCP Inspector
# Visit http://localhost:3000/mcp
```

### 2. Testing with Playground

The Smithery Playground provides a complete testing environment:
- Chat interface on left
- App panel on right (automatically opens when tool returns app)
- Theme switching
- Display mode controls

**App panel features:**
- Opens automatically when tool has `openai/outputTemplate`
- Manual refresh button to reload app HTML
- Multiple apps can be stored (switch between them)
- State persists across panel close/reopen

**Known limitation:**
- Playground currently has issues with BrowserRouter - use MemoryRouter for routing instead

### 3. Build for Production

```bash
# Build both server and client
npm run build

# Creates:
# - Bundled server code
# - Bundled app JS in .smithery/
```

---

## Common Issues & Solutions

### App doesn't render

**Check:**
1. Tool has `_meta["openai/outputTemplate"]` with correct URI
2. Resource is registered with matching URI
3. `smithery.yaml` has `type: widget`
4. App component exports as default

### Tool calls fail from app

**Check:**
1. Tool has `_meta["openai/widgetAccessible"]: true`
2. Using `useCallTool` hook correctly
3. Tool name matches registered tool
4. Arguments match tool's inputSchema

### State doesn't persist

**Check:**
1. Using `useWidgetState()` not `useState()`
2. State object is under 4k tokens
3. State is serializable (no functions, circular refs)

### Theme not applying

**Check:**
1. Using `useTheme()` hook
2. Applying theme class/styles in component
3. CSS supports both light and dark themes

---

## Best Practices

### Performance
- Keep `structuredContent` minimal (model reasoning only)
- Put full datasets in `_meta` (app UI only)
- Tree-shake unused dependencies
- Lazy-load heavy libraries

### Reliability
- Always handle loading states (`if (!state) return <Loading />`)
- Add error boundaries for app crashes
- Null-check all data before rendering
- Handle tool call errors gracefully

### UX
- Support both light and dark themes
- Adapt layout to display mode (inline vs fullscreen)
- Show loading indicators during async operations
- Provide clear error messages
- Make touch-friendly (buttons large enough, proper spacing)

### Data Management
- `structuredContent`: Summary for model (e.g., counts, names, IDs)
- `_meta`: Full objects for app (e.g., descriptions, URLs, nested data)
- `widgetState`: User preferences and selections only
- Keep widgetState lean (< 4k tokens)

---

## Quick Reference

### Server API

```typescript
import { widget } from "@smithery/sdk"

// Create widget resource
const myWidget = widget.resource<StateType>({
  name: "my-widget",
  description: "App description",
})

// Register with server
server.registerResource(
  myWidget.name,
  myWidget.uri,
  {},
  myWidget.handler
)

// Tool metadata
_meta: myWidget.toolConfig({
  invoking: "Loading...",
  invoked: "Done!",
})

// Tool response
return myWidget.response({
  structuredData,
  message: "Text for conversation",
  meta: { /* extra data */ }
})
```

### Client Hooks

```typescript
import {
  useToolOutput,          // Tool response data
  useToolInput,           // Tool arguments
  useToolResponseMetadata, // _meta field
  useWidgetState,         // Persistent state
  useCallTool,            // Call tools
  useSendFollowUp,        // Send messages
  useTheme,               // Theme
  useDisplayMode,         // Display mode
  useRequestDisplayMode,  // Request display change
  useMaxHeight,           // Max height
  useLocale,              // User locale
  useSafeArea,            // Safe area insets
  useUserAgent,           // Device info
} from "@smithery/sdk/react"
```

---

## Complete Example

### Server

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { widget } from "@smithery/sdk"
import type { GameState } from "./types.js"

export default function createServer() {
  const server = new McpServer({
    name: "Tic Tac Toe",
    version: "1.0.0",
  })

  const gameWidget = widget.resource<GameState>({
    name: "game",
    description: "Interactive tic-tac-toe game",
  })

  server.registerResource(
    gameWidget.name,
    gameWidget.uri,
    {},
    gameWidget.handler
  )

  server.registerTool(
    "make-move",
    {
      title: "Make Move",
      description: "Place X or O on the board",
      inputSchema: {
        position: z.number().min(0).max(8).describe("Position (0-8)"),
      },
      _meta: gameWidget.toolConfig({
        invoking: "Making move...",
        invoked: "Move made!",
      }),
    },
    async (args) => {
      const { position } = args
      
      // Game logic here
      const newBoard = makeMove(position)
      
      return gameWidget.response({
        structuredData: {
          board: newBoard,
          currentPlayer: "O",
          winner: null,
        },
        message: `Placed X at position ${position}`,
      })
    }
  )

  return server.server
}
```

### Client

```typescript
import { useToolOutput, useCallTool, useTheme } from "@smithery/sdk/react"
import type { GameState } from "../../server/types.js"

export default function Game() {
  const { structuredContent: state } = useToolOutput<GameState>()
  const makeMove = useCallTool<{ position: number }, GameState>("make-move")
  const theme = useTheme()

  if (!state) {
    return <div className={theme}>Loading game...</div>
  }

  const handleMove = async (pos: number) => {
    if (state.board[pos] || state.winner) return
    await makeMove.call({ position: pos })
  }

  return (
    <div className={`game ${theme}`}>
      <div className="board">
        {state.board.map((cell, i) => (
          <button
            key={i}
            onClick={() => handleMove(i)}
            disabled={cell !== null || makeMove.isPending}
          >
            {cell}
          </button>
        ))}
      </div>
      {state.winner && <div className="winner">Winner: {state.winner}</div>}
      {makeMove.error && <div className="error">{makeMove.error.message}</div>}
    </div>
  )
}
```

---

## Resources

- **OpenAI Apps SDK**: https://developers.openai.com/apps-sdk/
- **Smithery Docs**: https://smithery.ai/docs
- **MCP Protocol**: https://modelcontextprotocol.io

### Example Apps

- **Tic Tac Toe**: https://github.com/smithery-ai/sdk/tree/main/examples/open-ai-tic-tac-toe - Interactive game with widget state
- **Cafe Explorer**: https://github.com/smithery-ai/sdk/tree/main/examples/open-ai-cafe-explorer - Map-based exploration app

