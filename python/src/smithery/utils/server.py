"""Shared server utilities for Smithery CLI commands.

This module contains common server configuration and startup logic
to avoid duplication between dev.py and start.py.
"""

import sys
from importlib import import_module

from ..server.fastmcp_patch import SmitheryFastMCP


def configure_server_settings(
    server: SmitheryFastMCP,
    *,
    port: int,
    host: str,
    log_level: str
) -> None:
    """Configure server settings in a consistent way.

    Args:
        server: The FastMCP server instance
        port: Port to bind to
        host: Host to bind to
        log_level: Log level to use
    """
    server.settings.port = port
    server.settings.host = host
    server.settings.log_level = log_level


def create_server_from_ref(server_ref: str) -> SmitheryFastMCP:
    """Create server instance from module:function reference.

    Args:
        server_ref: Reference like "my_server.server:create_server"

    Returns:
        Configured server instance

    Raises:
        SystemExit: If server creation fails
    """
    try:
        module_path, function_name = server_ref.split(":", 1)
        module = import_module(module_path)
        server_function = getattr(module, function_name)
        server = server_function()

        if not hasattr(server, 'run'):
            print("Server function must return a FastMCP server instance", file=sys.stderr)
            sys.exit(1)

        return server

    except Exception as e:
        print(f"Failed to create server from {server_ref}: {e}", file=sys.stderr)
        sys.exit(1)


def run_server(
    server: SmitheryFastMCP,
    transport: str,
    *,
    port: int,
    host: str,
    log_level: str
) -> None:
    """Run server with the specified transport configuration.

    Args:
        server: The server instance to run
        transport: Transport type ("shttp" or "stdio")
        port: Port for shttp transport
        host: Host for shttp transport
        log_level: Log level to use
    """
    if transport == "shttp":
        configure_server_settings(server, port=port, host=host, log_level=log_level)
        server.run(transport="streamable-http")
    elif transport == "stdio":
        configure_server_settings(server, port=0, host="", log_level=log_level)
        server.run(transport="stdio")
    else:
        print(f"Unsupported transport: {transport}", file=sys.stderr)
        sys.exit(1)


def check_port_available(host: str, port: int) -> bool:
    """Check if a port is available for binding.

    Args:
        host: Host to check
        port: Port to check

    Returns:
        True if port is available, False otherwise
    """
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
        return True
    except OSError:
        return False
