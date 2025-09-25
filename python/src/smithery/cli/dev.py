"""
Smithery Python Development Server

Development server with reload support and flexible port handling.
"""

import argparse
import os
import sys

from ..utils.console import console
from ..utils.network import find_available_port
from ..utils.project import get_server_ref_from_config
from ..utils.server import create_server_from_ref, run_server


def run_dev_server(
    server_ref: str | None = None,
    transport: str = "shttp",
    port: int = 8081,
    host: str = "127.0.0.1",
    reload: bool = True,
    log_level: str = "info"
) -> int:
    """Run development server with reload and flexible port handling.

    Returns:
        The actual port used (may differ from requested due to port availability)
    """
    try:
        # Get server reference
        if server_ref is None:
            server_ref = get_server_ref_from_config()

        # Create server
        server = create_server_from_ref(server_ref)

        if transport == "shttp":
            try:
                actual_port = find_available_port(port, host)
                if actual_port != port:
                    console.warning(f"Port {port} is in use, using port {actual_port} instead")
                    port = actual_port
            except RuntimeError as e:
                console.error(f"Could not find an available port: {e}")
                sys.exit(1)

            if reload:
                try:
                    import uvicorn  # type: ignore
                except ImportError:
                    console.error("Reload requested but 'uvicorn' is not installed")
                    console.nested("Install it in your project environment:")
                    console.indented("uv add uvicorn  # or: pip install uvicorn")
                    sys.exit(1)

                # Pass server ref for reloader
                if server_ref:
                    os.environ["SMITHERY_SERVER_REF"] = server_ref

                # Use uvicorn with reload
                uvicorn.run(
                    "smithery.cli.dev:get_reloader_streamable_http_app",
                    host=host,
                    port=port,
                    reload=True,
                    factory=True,
                    log_level=log_level,
                )
            else:
                # No reload - same as production
                run_server(server, "shttp", port=port, host=host, log_level=log_level)

            return port

        elif transport == "stdio":
            # Same as production
            run_server(server, transport, port=0, host="", log_level=log_level)
            return 0

        else:
            console.error(f"Unsupported transport: {transport}")
            console.nested("Supported transports: shttp, stdio")
            sys.exit(1)

    except KeyboardInterrupt:
        console.info("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to run server: {e}")
        sys.exit(1)

# Factory used by uvicorn --reload (import-string target)
def get_reloader_streamable_http_app():
    """Return a fresh ASGI app for streamable HTTP using env SMITHERY_SERVER_REF.

    This function is imported by Uvicorn in a fresh interpreter on reload.
    """
    server_ref = os.environ.get("SMITHERY_SERVER_REF")
    if not server_ref:
        raise RuntimeError("SMITHERY_SERVER_REF not set for reloader")

    # Create server using same logic as production
    server = create_server_from_ref(server_ref)
    return server.streamable_http_app()


def main():
    """Entry point for the dev script."""
    parser = argparse.ArgumentParser(description="Run MCP server in development mode")
    parser.add_argument("server_function", nargs="?", help="Server function (e.g., src.server:create_server)")
    parser.add_argument("--transport", default="shttp", help="Transport type (shttp or stdio)")
    parser.add_argument("--port", type=int, default=8081, help="Port to run on (shttp only)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (shttp only)")
    parser.add_argument("--reload", dest="reload", action="store_true", default=True, help="Enable auto-reload (shttp only, requires uvicorn)")
    parser.add_argument("--no-reload", dest="reload", action="store_false", help="Disable auto-reload")
    parser.add_argument("--log-level", default="info", help="Log level (critical, error, warning, info, debug, trace)")

    args = parser.parse_args()
    run_dev_server(
        server_ref=args.server_function,
        transport=args.transport,
        port=args.port,
        host=args.host,
        reload=args.reload,
        log_level=args.log_level.lower()
    )


if __name__ == "__main__":
    # For direct execution: python -m smithery.cli.dev
    main()
