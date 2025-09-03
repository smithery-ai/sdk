#!/usr/bin/env python3
"""
Smithery Python MCP Server Bootstrap (HTTP Transport)
This file is injected by the Smithery build system.
"""

import os
import sys
from importlib import import_module
from typing import Any


def import_server_module(server_ref: str) -> dict[str, Any]:
    """Import the server module and extract components (inlined for self-containment)."""
    try:
        # Extract module path, ignore function name (always use 'default')
        module_path = server_ref.split(":")[0] if ":" in server_ref else server_ref
        module = import_module(module_path)

        # Require default export (like TypeScript)
        if not hasattr(module, 'default') or not callable(module.default):
            raise AttributeError("Module must export 'default' function")

        default_fn = module.default
        config_schema = getattr(module, 'config_schema', None)

        print("[smithery] Setting up server")
        if config_schema:
            # Check if it's a Pydantic model (duck typing to avoid importing pydantic)
            if hasattr(config_schema, '__name__'):
                print(f"[smithery] Using config schema: {config_schema.__name__}")

        return {
            'default': default_fn,
            'config_schema': config_schema,
        }
    except Exception as e:
        print(f"✗ Failed to import server module '{server_ref}': {e}", file=sys.stderr)
        print("✗ Expected module contract:")
        print("  - default = function(config) -> FastMCP  # Required")
        print("  - config_schema = class(BaseModel)  # Optional")
        sys.exit(1)


def main():
    """Main entry point for the MCP server."""
    try:
        # Server reference will be injected by build system
        server_ref = "src.server:default"

        print("[smithery] Starting Python MCP server...")
        print(f"[smithery] Loading server from: {server_ref}")

        # Import server components
        components = import_server_module(server_ref)
        default_fn = components['default']
        config_schema = components['config_schema']

        # Create config instance
        config = {}
        if config_schema:
            config = config_schema()

        # Create server instance
        server = default_fn(config)

        # Get port from environment or default
        port = int(os.environ.get("PORT", "8081"))
        server.settings.port = port

        print(f"✓ [smithery] MCP server starting on port {port}")

        # Run with streamable HTTP transport
        server.run(transport="streamable-http")

    except Exception as e:
        print(f"✗ [smithery] Failed to start MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
