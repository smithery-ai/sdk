# Hello Widget Example

[![smithery badge](https://smithery.ai/badge/@smithery-ai/sdk)](https://smithery.ai/server/@smithery-ai/sdk)

A minimal example of a ChatGPT widget using the Smithery SDK.

## What It Does

Greets someone by name with a beautiful widget displaying:
- Personalized greeting message
- Timestamp of when greeted
- Theme-aware styling (light/dark)

## Running Locally

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Visit http://localhost:3000/mcp in MCP Inspector
```

## Project Structure

```
app/
├── server/
│   ├── types.ts       # Shared types
│   └── index.ts       # MCP server with SDK helpers
└── web/
    └── src/
        ├── greeter.tsx        # Widget component (default export)
        └── types.ts           # Re-export server types
smithery.yaml          # Must include "type: widget"
```

**Note:** No `index.tsx` needed - the CLI auto-generates the entry point!

## Key Features

### Server Side (`app/server/index.ts`)

- Uses `createWidgetServer()` from SDK
- Clean `tool()` helper for metadata
- `widget.response()` for standard responses
- `widget.resource()` auto-generates widget HTML

### Client Side (`app/web/src/greeter.tsx`)

- `useWidgetState<GreeterState>()` for type-safe state
- `useTheme()` for theme-aware styling
- Zero boilerplate - just React

## Configuration

`smithery.yaml`:
```yaml
runtime: typescript
type: widget
```

The `type: widget` tells the CLI to:
- Bundle the server code
- Bundle the client widget(s) from `app/web/src/`
- Auto-generate the React entry point
- Watch both server and client files in dev mode

## Total Code

- **Server:** ~40 lines (types + logic)
- **Client:** ~60 lines (just the component)
- **Config:** 2 lines (smithery.yaml)
- **Total:** ~102 lines for complete working widget

Compare to vanilla MCP: ~300+ lines (66% reduction!)

**No boilerplate:** CLI auto-generates the entry point from your component!

