"""
Smithery Python Playground

Interactive playground that runs the MCP server and connects the Smithery CLI client.
"""

import subprocess
import sys
import threading
import time

from ..utils.console import console
from .dev import run_server


def main() -> None:
    """CLI entry point for playground command."""

    import typer

    app = typer.Typer()

    @app.command()
    def playground_cmd(
        server_function: str | None = typer.Argument(None, help="Server function (e.g., src.server:create_server)"),
        port: int = typer.Option(8081, help="Port to run on")
    ):
        """Start your MCP server and automatically connect the Smithery CLI client for interactive testing."""
        start_playground(server_function, port)

    app()


def start_playground(server_function: str | None, port: int) -> None:
    """Start the playground with given parameters."""
    from ..utils.project import get_server_ref_from_config
    from .dev import find_available_port

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

    console.info(f"Starting playground on port {actual_port}...")
    console.info("This will run your MCP server and connect the Smithery CLI client")
    console.plain("")

    # Start server in background thread with the resolved port
    def start_server():
        try:
            run_server(server_ref, "shttp", actual_port, "127.0.0.1")
        except Exception as e:
            console.error(f"Server failed: {e}")

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait a moment for server to start
    console.info("Waiting for server to start...")
    time.sleep(2)

    # Start Smithery CLI client with the same resolved port
    try:
        console.info(f"Starting Smithery CLI client connected to port {actual_port}")
        subprocess.run([
            "npx", "-y", "@smithery/cli", "playground", "--port", str(actual_port)
        ], check=True)
    except KeyboardInterrupt:
        console.info("Playground stopped by user")
        console.plain("")
        console.info("🚀 Deploy this server: https://smithery.ai/new")
    except subprocess.CalledProcessError as e:
        console.error(f"Failed to start Smithery CLI: {e}")
        console.info("Make sure you have Node.js installed and @smithery/cli is available")
    except FileNotFoundError:
        console.error("npx not found. Please install Node.js to use the playground")
        sys.exit(1)


if __name__ == "__main__":
    main()
