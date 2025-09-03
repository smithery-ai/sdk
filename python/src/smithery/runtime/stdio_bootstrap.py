#!/usr/bin/env python3
"""
Smithery Python MCP Server Bootstrap (STDIO Transport)
This file is injected by the Smithery build system.
"""

import sys
from smithery.cli.build import import_server_module


def main():
    """Main entry point for the MCP server."""
    try:
        # Server reference will be injected by build system
        server_ref = "SMITHERY_SERVER_REF"
        
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
        
        # Run with stdio transport
        server.run(transport="stdio")
        
    except Exception as e:
        print(f"✗ [smithery] Failed to start MCP server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
