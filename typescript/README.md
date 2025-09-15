# Smithery TypeScript SDKs

This directory contains three TypeScript packages for building and managing MCP servers with Smithery:

## Packages

### [`registry/`](./registry/)
The **Registry SDK** - A TypeScript client for interacting with the Smithery Registry API.

### [`sdk/`](./sdk/)
The **Smithery SDK** - A library with utilities to help developers build and use MCP servers.

### [`create/`](./create/)
**Scaffold** - CLI for bootstrapping new MCP server projects.
- Published as [`create-smithery`](https://www.npmjs.com/package/create-smithery) on npm
- Usage: `npm create smithery `

## Quick Start

```bash
# Create a new MCP server project
npm create smithery

# Install the SDK in an existing project
npm install @smithery/sdk

# Install the Registry API client
npm install @smithery/registry
```
