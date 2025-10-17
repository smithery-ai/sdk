# Hello Widget Example

A minimal ChatGPT app with interactive greeting widget, confetti animation, and theme support.

Built with [Smithery CLI](https://smithery.ai/docs)

## Prerequisites

- **Smithery API key**: Get yours at [smithery.ai/account/api-keys](https://smithery.ai/account/api-keys)

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start smithery playground:
   ```bash
   npm run dev
   ```

Try asking: "Say hello to Alice"

## Development

Your code is organized as:
- `app/server/` - MCP server with widget resource
- `app/shared/` - Shared TypeScript types
- `app/web/src/` - React widget component

Edit `app/web/src/greeter.tsx` to customize the widget UI.

## Build

```bash
npm run build
```

Creates bundled server and widget JS in `.smithery/`

## Deploy

Ready to deploy? Push your code to GitHub and deploy to Smithery:

1. Create a new repository at [github.com/new](https://github.com/new)

2. Initialize git and push to GitHub:
   ```bash
   git add .
   git commit -m "Hello widget"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. Deploy your app to Smithery at [smithery.ai/new](https://smithery.ai/new)

## Learn More

- [Smithery Docs](https://smithery.ai/docs)
- [MCP Protocol](https://modelcontextprotocol.io)
