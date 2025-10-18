# Local Filesystem MCP Server

A Model Context Protocol (MCP) server for exploring local filesystems with glob and grep tools.

Built with [Smithery SDK](https://smithery.ai/docs)

## Features

This server provides two essential tools for filesystem exploration:

- **glob** - Find files matching patterns (e.g., `**/*.ts`, `src/**/*.js`)
- **grep** - Search for text patterns in files

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

The server will run locally and provide access to your filesystem through the MCP protocol.

## Configuration

You can customize the working directory in your `smithery.yaml` config:

```yaml
runtime: typescript
target: local
config:
  workingDirectory: /path/to/your/directory
```

By default, it uses the current working directory.

## Development

Your code is organized as:
- `src/index.ts` - MCP server with glob and grep tools
- `smithery.yaml` - Runtime specification with `target: local` for filesystem access

Edit `src/index.ts` to add your own filesystem tools.

## Build

```bash
npm run build
```

Creates bundled server in `.smithery/`

## Deploy

This server uses `target: local` in `smithery.yaml`, which means it's designed to run locally with filesystem access. It cannot be deployed to remote Smithery hosting.

## Learn More

- [Smithery Docs](https://smithery.ai/docs)
- [MCP Protocol](https://modelcontextprotocol.io)

