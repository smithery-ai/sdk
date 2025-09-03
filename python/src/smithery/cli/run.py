"""
Smithery Python Run System
===========================

Command-line interface for running Smithery Python MCP servers.
"""

import argparse
import sys
from typing import Any

from rich.console import Console

from .build import get_server_ref_from_config, import_server_module

# Initialize rich console
console = Console()


def run_server(server_ref: str, transport: str = "shttp", port: int = 8081, host: str = "127.0.0.1") -> None:
    """
    Run a Smithery MCP server directly without building a separate file.

    Args:
        server_ref: Module reference in format 'module.path:function'
        transport: Transport type ('shttp' or 'stdio')
        port: Port to run on (shttp only)
        host: Host to bind to (shttp only)
    """
    console.print(f"[cyan][smithery][/cyan] Starting Python MCP server with {transport} transport...")
    console.print(f"[cyan][smithery][/cyan] Server reference: {server_ref}")

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
                console.print(f"[cyan][smithery][/cyan] Using config schema: {config_schema.__name__}")
            except Exception as e:
                console.print(f"[yellow]⚠ Warning: Failed to instantiate config schema: {e}[/yellow]")
                console.print("[yellow]⚠ Proceeding with empty config[/yellow]")

        # Create server instance
        console.print("[cyan][smithery][/cyan] Creating server instance...")
        server = create_server(config)

        if transport == "shttp":
            # Set server configuration for HTTP transport
            server.settings.port = port
            server.settings.host = host

            console.print(f"[cyan][smithery][/cyan] MCP server starting on {host}:{port}")
            console.print("[cyan][smithery][/cyan] Transport: streamable HTTP")

            # Run with streamable HTTP transport
            server.run(transport="streamable-http")

        elif transport == "stdio":
            console.print("[cyan][smithery][/cyan] MCP server starting with stdio transport")

            # Run with stdio transport
            server.run(transport="stdio")

        else:
            raise ValueError(f"Unsupported transport: {transport}")

    except KeyboardInterrupt:
        console.print("\n[cyan][smithery][/cyan] Server stopped by user")
        sys.exit(0)
    except Exception as e:
        console.print(f"[cyan][smithery][/cyan] Failed to start MCP server: {e}", file=sys.stderr)
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
