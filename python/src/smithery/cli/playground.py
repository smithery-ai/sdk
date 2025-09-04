"""
Smithery Python Playground Command
==================================

Interactive playground that runs the MCP server and connects the Smithery CLI client.
"""

import subprocess
import sys
import threading
import time

from ..utils.console import console
from .run import run_server


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
    from .helpers import get_server_ref_from_config

    # Get server reference from config if not provided
    server_ref = server_function or get_server_ref_from_config()

    console.info(f"Starting playground on port {port}...")
    console.info("This will run your MCP server and connect the Smithery CLI client")
    console.plain("")

    # Start server in background thread
    def start_server():
        try:
            run_server(server_ref, "shttp", port, "127.0.0.1")
        except Exception as e:
            console.error(f"Server failed: {e}")

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait a moment for server to start
    console.info("Waiting for server to start...")
    time.sleep(2)

    # Start Smithery CLI client
    try:
        console.info(f"Starting Smithery CLI client connected to port {port}")
        subprocess.run([
            "npx", "-y", "@smithery/cli", "--port", str(port)
        ], check=True)
    except KeyboardInterrupt:
        console.info("Playground stopped by user")
    except subprocess.CalledProcessError as e:
        console.error(f"Failed to start Smithery CLI: {e}")
        console.info("Make sure you have Node.js installed and @smithery/cli is available")
    except FileNotFoundError:
        console.error("npx not found. Please install Node.js to use the playground")
        sys.exit(1)


if __name__ == "__main__":
    main()
