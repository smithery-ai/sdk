"""Network utilities for Smithery Python SDK."""

import socket


def find_available_port(preferred_port: int = 8081, host: str = "127.0.0.1", max_attempts: int = 100) -> int:
    """Find an available port, starting with the preferred port.

    Args:
        preferred_port: The port to try first
        host: The host to bind to when checking port availability
        max_attempts: Maximum number of ports to try before giving up

    Returns:
        An available port number

    Raises:
        RuntimeError: If no available port is found within max_attempts
    """
    for port_offset in range(max_attempts):
        port = preferred_port + port_offset
        if is_port_available(port, host):
            return port

    raise RuntimeError(f"Could not find an available port starting from {preferred_port} after {max_attempts} attempts")


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a port is available for binding.

    Args:
        port: The port number to check
        host: The host to bind to when checking

    Returns:
        True if the port is available, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            return True
    except OSError:
        return False
