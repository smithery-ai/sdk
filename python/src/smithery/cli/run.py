"""
Smithery Python Run System
===========================

Command-line interface for running Smithery Python MCP servers.
"""

import sys
from typing import Any

from ..utils.console import console
from .build import import_server_module
from .helpers import create_base_parser, get_server_ref_from_config


def run_server(server_ref: str, transport: str = "shttp", port: int = 8081, host: str = "127.0.0.1") -> None:
    """Run Smithery MCP server directly."""
    console.info(f"Starting Python MCP server with {transport} transport...")
    console.info(f"Server reference: {server_ref}")

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
                console.info(f"Using config schema: {config_schema.__name__}")
            except Exception as e:
                console.warning(f"Failed to instantiate config schema: {e}")
                console.warning("Proceeding with empty config")

        # Create server instance
        console.info("Creating server instance...")
        server = create_server(config)

        if transport == "shttp":
            # Set server configuration for HTTP transport
            server.settings.port = port
            server.settings.host = host

            console.info(f"MCP server starting on {host}:{port}")
            console.info("Transport: streamable HTTP")

            # Run with streamable HTTP transport
            server.run(transport="streamable-http")

        elif transport == "stdio":
            console.info("MCP server starting with stdio transport")

            # Run with stdio transport
            server.run(transport="stdio")

        else:
            raise ValueError(f"Unsupported transport: {transport}")

    except KeyboardInterrupt:
        console.info("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to start MCP server: {e}")
        sys.exit(1)


def main() -> None:
    """CLI entry point for run command."""
    parser = create_base_parser(
        prog="smithery run",
        description="Run Smithery MCP servers directly (like uvicorn)",
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
