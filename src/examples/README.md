# Examples

This directory contains examples demonstrating how to use the Smithery SDK.

## Running the Examples

1. First, make sure you have the required environment variables:

   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export E2B_API_KEY="your-e2b-api-key"
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Build the SDK:

   ```bash
   npm run build
   ```

4. Run an example:
   ```bash
   # Run the simple example
   npx tsx examples/simple.ts
   ```

## Available Examples

### simple.ts

A basic example that shows how to:

- Connect to an MCP (e2b in this case)
- Patch an OpenAI client
- Have a conversation that uses MCP tools
- Handle multi-step tool execution
