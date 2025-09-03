#!/usr/bin/env python3
"""
Smithery Python MCP Server Bootstrap (HTTP Transport)
This file is injected by the Smithery build system.
"""

import os
import sys
# This import will be replaced by the build system
from smithery.virtual.user_module import default, config_schema


def main():
    """Main entry point for the MCP server."""
    try:
        print(f"[smithery] Starting Python MCP server...")
        
        # Server function and config schema imported at module level
        server_fn = default
        server_config_schema = config_schema
        
        # Create config instance
        config = {}
        if server_config_schema:
            config = server_config_schema()
        
        # Create server instance
        server = server_fn(config)
        
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
