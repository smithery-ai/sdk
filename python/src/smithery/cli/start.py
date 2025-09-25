"""Production server start for Smithery Python MCP servers."""

import argparse
import sys

from ..utils.server import check_port_available, create_server_from_ref, run_server


def run_production_server(
    server_ref: str | None = None,
    port: int = 8081,
    host: str = "127.0.0.1"
) -> None:
    """Start server with minimal overhead."""
    try:
        # Default log level for production
        log_level = "warning"

        if server_ref is None:
            import tomllib
            with open("pyproject.toml", "rb") as f:
                config = tomllib.load(f)
                smithery_config = config["tool"]["smithery"]
                server_ref = smithery_config["server"]

                # Get log_level from config (production is config-driven)
                log_level = smithery_config.get("log_level", "warning")

        # Create server instance
        server = create_server_from_ref(server_ref)

        # Check port availability for production
        if not check_port_available(host, port):
            print(f"Port {port} unavailable on {host}", file=sys.stderr)
            sys.exit(1)

        # Run server with shttp transport
        run_server(server, "shttp", port=port, host=host, log_level=log_level)

    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Entry point for the start script."""
    parser = argparse.ArgumentParser(description="Start MCP server for production use")
    parser.add_argument("server_function", nargs="?", help="Server function (e.g., src.server:create_server)")
    parser.add_argument("--port", type=int, default=8081, help="Port to run on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")

    args = parser.parse_args()
    run_production_server(
        server_ref=args.server_function,
        port=args.port,
        host=args.host
    )


if __name__ == "__main__":
    # For direct execution: python -m smithery.cli.start
    main()
