"""
Smithery Python Run System
===========================

Command-line interface for running Smithery Python MCP servers.
"""

import argparse
import os
import sys
from typing import Any

import colorama
from colorama import Fore, Style

from .build import import_server_module, get_server_ref_from_config

# Initialize colorama for cross-platform color support
colorama.init()


def run_server(server_ref: str, transport: str = "shttp", port: int = 8081, host: str = "127.0.0.1") -> None:
    """
    Run a Smithery MCP server directly without building a separate file.
    
    Args:
        server_ref: Module reference in format 'module.path:function'
        transport: Transport type ('shttp' or 'stdio')  
        port: Port to run on (shttp only)
        host: Host to bind to (shttp only)
    """
    print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Starting Python MCP server with {transport} transport...")
    print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Server reference: {server_ref}")
    
    try:
        # Import and validate server module
        server_module = import_server_module(server_ref)
        create_server = server_module['create_server']
        config_schema = server_module.get('config_schema')
        
        # Create config instance
        config: Any = {}
        if config_schema:
            try:
                config = config_schema()
                print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Using config schema: {config_schema.__name__}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ Warning: Failed to instantiate config schema: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}⚠ Proceeding with empty config{Style.RESET_ALL}")
        
        # Create server instance
        print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Creating server instance...")
        server = create_server(config)
        
        if transport == "shttp":
            # Set server configuration for HTTP transport
            server.settings.port = port
            server.settings.host = host
            
            print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} MCP server starting on {host}:{port}")
            print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Transport: streamable HTTP")
            
            # Run with streamable HTTP transport
            server.run(transport="streamable-http")
            
        elif transport == "stdio":
            print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} MCP server starting with stdio transport")
            
            # Run with stdio transport
            server.run(transport="stdio")
            
        else:
            raise ValueError(f"Unsupported transport: {transport}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}[smithery]{Style.RESET_ALL} Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.CYAN}[smithery]{Style.RESET_ALL} Failed to start MCP server: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """CLI entry point for Smithery Python run system."""
    parser = argparse.ArgumentParser(
        description="Run Smithery MCP servers directly (like uvicorn)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery run                          # Read from pyproject.toml [tool.smithery].server
  smithery run src.server:create_server # Run specific server function
  smithery run --transport stdio        # Run with stdio transport
  smithery run --port 3000              # Run on custom port (shttp only)
        """
    )

    parser.add_argument(
        "server_ref",
        nargs="?",
        help="Server reference (module:function). Read from pyproject.toml [tool.smithery].server if not provided."
    )
    parser.add_argument(
        "--transport",
        choices=["shttp", "stdio"],
        default="shttp",
        help="Transport type (default: shttp)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8081,
        help="Port to run on (shttp only, default: 8081)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (shttp only, default: 127.0.0.1)"
    )

    args = parser.parse_args()

    # Get server reference from config if not provided explicitly
    server_ref = args.server_ref or get_server_ref_from_config()

    run_server(server_ref, args.transport, args.port, args.host)


if __name__ == "__main__":
    main()
