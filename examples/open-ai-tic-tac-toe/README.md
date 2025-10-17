# Tic-Tac-Toe Widget Example

An interactive tic-tac-toe game widget using the Smithery SDK.

## What It Does

Play tic-tac-toe with an AI in ChatGPT with a beautiful interactive widget:
- Click cells to make moves
- Visual game board with X and O markers
- Automatic turn tracking
- Win/draw detection
- Theme-aware styling (light/dark mode)
- Responsive design for inline and fullscreen modes

## Running Locally

```bash
# Install dependencies
npm install

# Build the widget bundle
cd app/web && npm install && npm run build && cd ../..

# Start development server
npm run dev

# Visit http://localhost:3000/mcp in MCP Inspector
```

## Project Structure

```
app/
├── server/
│   ├── types.ts       # Shared types (GameState, CellValue)
│   └── index.ts       # MCP server with SDK helpers
└── web/
    └── src/
        ├── tic-tac-toe.tsx   # Widget component
        └── index.tsx         # Entry point
smithery.yaml          # Must include "type: widget"
```

## Key Features

### Server Side (`app/server/index.ts`)

- Uses `widget.resource()` for clean widget registration
- Uses `widget.toolConfig()` for tool metadata
- Uses `widget.response()` for structured responses
- Uses `widget.error()` for error responses
- Stateful game logic with win/draw detection

### Client Side (`app/web/src/tic-tac-toe.tsx`)

- Uses `useTheme()` for theme-aware styling
- Uses `useDisplayMode()` for responsive layouts
- Uses `useMaxHeight()` for proper sizing
- Uses `useToolResponseMetadata()` for game state
- Direct tool calls via `window.openai.callTool()`

## Tools

### `start-game`
Start a new tic-tac-toe game

### `make-move`
Make a move at a specific position (0-8)
- Position 0-2: Top row
- Position 3-5: Middle row
- Position 6-8: Bottom row

### `get-game-state`
Get the current state of the game

## Game Logic

The server maintains game state and implements:
- Win condition checking (rows, columns, diagonals)
- Draw detection (board full)
- Turn management (alternating X and O)
- Move validation (occupied cells, game over)

## Widget Features

- **Interactive Cells**: Click any empty cell to make a move
- **Status Display**: Shows current player or game result
- **New Game Button**: Reset/start a new game anytime
- **Theme Support**: Adapts to light/dark mode
- **Display Modes**: Optimized for inline and fullscreen

## Configuration

`smithery.yaml`:
```yaml
runtime: typescript
type: widget
```

The `type: widget` tells the CLI to:
- Bundle the server code
- Bundle the client widget from `app/web/src/`
- Watch both server and client files in dev mode

