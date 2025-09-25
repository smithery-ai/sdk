"""
Smithery Python Playground

Interactive playground that runs the MCP server and connects the Smithery CLI client.
"""

import argparse
import subprocess
import threading
import time

from ..utils.console import console
from .dev import run_dev_server


def start_playground(server_function: str | None, port: int, reload: bool = False) -> None:
    """Start the playground with given parameters."""
    from ..utils.network import find_available_port
    from ..utils.project import get_server_ref_from_config

    # Get server reference from config if not provided
    server_ref = server_function or get_server_ref_from_config()

    # Resolve port upfront - this ensures both server and client use the same port
    try:
        actual_port = find_available_port(port, "127.0.0.1")
        if actual_port != port:
            console.warning(f"Port {port} is in use, using port {actual_port} instead")
    except RuntimeError as e:
        console.error(f"Could not find an available port: {e}")
        return

    # Start Smithery CLI client in background with the resolved port
    def start_playground_client():
        # Wait a moment for server to start
        time.sleep(2)
        try:
            console.info(f"Starting Smithery CLI client connected to port {actual_port}")
            subprocess.run([
                "npx", "-y", "@smithery/cli", "playground", "--port", str(actual_port)
            ], check=True)
        except subprocess.CalledProcessError as e:
            console.error(f"Failed to start Smithery CLI: {e}")
            console.info("Make sure you have Node.js installed and @smithery/cli is available")
        except FileNotFoundError:
            console.error("npx not found. Please install Node.js to use the playground")

    # Start playground client in background thread
    client_thread = threading.Thread(target=start_playground_client, daemon=True)
    client_thread.start()

    # Show reload warning if enabled
    if reload:
        console.warning(
            "Note: hot reload resets in-memory server state; stateful clients may need to reinitialize their session after a reload."
        )

    # Start server in main thread (this allows uvicorn reload to work properly)
    try:
        run_dev_server(server_ref, "shttp", actual_port, "127.0.0.1", reload=reload, log_level="warning")
    except KeyboardInterrupt:
        console.info("Playground stopped by user")
        console.plain("")
        console.info("🚀 Deploy this server: https://smithery.ai/new")
    except Exception as e:
        console.error(f"Server failed: {e}")


def main():
    """Entry point for the playground script."""
    parser = argparse.ArgumentParser(description="Run server and connect Smithery Playground for testing")
    parser.add_argument("server_function", nargs="?", help="Server function (e.g., src.server:create_server)")
    parser.add_argument("--port", type=int, default=8081, help="Port to run on")
    parser.add_argument("--reload", dest="reload", action="store_true", default=False, help="Enable auto-reload (requires uvicorn)")
    parser.add_argument("--no-reload", dest="reload", action="store_false", help="Disable auto-reload (default)")

    args = parser.parse_args()
    start_playground(args.server_function, args.port, args.reload)


if __name__ == "__main__":
    # For direct execution: python -m smithery.cli.playground
    main()
