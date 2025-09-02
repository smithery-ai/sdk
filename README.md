# Smithery SDK

[![npm version](https://img.shields.io/npm/v/%40smithery%2Fsdk?style=flat-square)](https://www.npmjs.com/package/@smithery/sdk) 
[![npm version](https://img.shields.io/npm/v/%40smithery%2Fregistry?style=flat-square)](https://www.npmjs.com/package/@smithery/registry) 
[![PyPI - Version](https://img.shields.io/pypi/v/smithery?style=flat-square)](https://pypi.org/project/smithery/)


Smithery SDK provides utilities to make it easier for you to develop and deploy [Model Context Protocols](https://modelcontextprotocol.io/) (MCPs) with Smithery.

**Key Features**

- **TypeScript**: Library functions to connect to Smithery MCPs and registry client
- **Python**: Enhanced FastMCP servers with session-scoped configuration support
- Adapters to transform MCP responses for OpenAI and Anthropic clients
- Docker-ready scaffolding for easy deployment

To find our registry of MCPs, visit [https://smithery.ai/](https://smithery.ai/).

## Languages

### TypeScript
- [Registry](typescript/registry/README.md) — find and connect to MCP servers in the registry
- [SDK](typescript/sdk/README.md) — build and deploy MCP servers to the registry

### Python
- [SDK](python/README.md) — enhanced FastMCP servers with session-scoped configuration
- [Scaffold](python/scaffold/) — ready-to-use MCP server template with Docker support