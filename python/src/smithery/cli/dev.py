"""
Smithery Python Development Server

Development server with reload support and flexible port handling.
"""

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
        # Get server reference (same as production)
        if server_ref is None:
            server_ref = get_server_ref_from_config()

        # Create server (same as production)
        server = create_server_from_ref(server_ref)

        if transport == "shttp":
            # DEV DIFFERENCE #1: Find available port instead of failing
            try:
                actual_port = find_available_port(port, host)
                if actual_port != port:
                    console.warning(f"Port {port} is in use, using port {actual_port} instead")
                    port = actual_port
            except RuntimeError as e:
                console.error(f"Could not find an available port: {e}")
                sys.exit(1)

            # DEV DIFFERENCE #2: Reload support
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


if __name__ == "__main__":
    # For direct execution: python -m smithery.cli.dev
    run_dev_server()
