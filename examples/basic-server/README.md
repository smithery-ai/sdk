# Basic MCP Server

A minimal Model Context Protocol (MCP) server demonstrating tools, resources, and prompts.

Built with [Smithery SDK](https://smithery.ai/docs)

## Prerequisites

- **Smithery API key**: Get yours at [smithery.ai/account/api-keys](https://smithery.ai/account/api-keys)

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

Try the `hello` tool, `history://hello-world` resource, or `greet` prompt.

## Development

Your code is organized as:
- `src/index.ts` - MCP server with tools, resources, and prompts
- `smithery.yaml` - Runtime specification

Edit `src/index.ts` to add your own tools, resources, and prompts.

## Build

```bash
npm run build
```

Creates bundled server in `.smithery/`

## Deploy

Ready to deploy? Push your code to GitHub and deploy to Smithery:

1. Create a new repository at [github.com/new](https://github.com/new)

2. Initialize git and push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. Deploy your server to Smithery at [smithery.ai/new](https://smithery.ai/new)

## Learn More

- [Smithery Docs](https://smithery.ai/docs)
- [MCP Protocol](https://modelcontextprotocol.io)

