#!/usr/bin/env python3
"""
Smithery Python MCP Server Bootstrap (HTTP Transport)
This file is injected by the Smithery build system.
"""

import os
import sys
from smithery.cli.build import import_server_module


def main():
    """Main entry point for the MCP server."""
    try:
        # Server reference will be injected by build system
        server_ref = "SMITHERY_SERVER_REF"
        
        print(f"[smithery] Starting Python MCP server...")
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
