#!/usr/bin/env python3
"""
Smithery Python MCP Server Bootstrap (HTTP Transport)
This file is injected by the Smithery build system.
"""

import os
import sys
from importlib import import_module
from colorama import Fore, Style


def main():
    """Main entry point for the MCP server."""
    try:
        # Module and function references injected at build time
        module_name = "$SMITHERY_MODULE"
        function_name = "$SMITHERY_FUNCTION"
        
        print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Starting Python MCP server...")
        print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Loading server from: {module_name}:{function_name}")
        
        # Ensure current directory is in Python path
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Runtime module resolution (like uvicorn main:app)
        module = import_module(module_name)
        server_fn = getattr(module, function_name)
        server_config_schema = getattr(module, 'config_schema', None)

        # Create config instance
        config = {}
        if server_config_schema:
            config = server_config_schema()

        # Create server instance
        server = server_fn(config)

        # Get port from environment or default
        port = int(os.environ.get("PORT", "8081"))
        server.settings.port = port

        print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} MCP server starting on port {port}")

        # Run with streamable HTTP transport
        server.run(transport="streamable-http")

    except Exception as e:
        print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Failed to start MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
