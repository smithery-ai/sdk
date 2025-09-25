"""Ultra-fast production server start for Smithery Python MCP servers."""

import sys


def run_production_server(
    server_ref: str | None = None,
    transport: str = "shttp",
    port: int = 8081,
    host: str = "127.0.0.1",
    log_level: str = "warning"
) -> None:
    """Start server with minimal overhead."""
    try:
        if server_ref is None:
            import tomllib
            with open("pyproject.toml", "rb") as f:
                server_ref = tomllib.load(f)["tool"]["smithery"]["server"]

        from importlib import import_module
        module_path, function_name = server_ref.split(":", 1)
        server = getattr(import_module(module_path), function_name)()

        if transport == "shttp":
            import socket
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.bind((host, port))
            except OSError:
                print(f"Port {port} unavailable on {host}", file=sys.stderr)
                sys.exit(1)

            server.settings.port = port
            server.settings.host = host
            server.run(transport="streamable-http")
        elif transport == "stdio":
            server.run(transport="stdio")
        else:
            print(f"Unsupported transport: {transport}", file=sys.stderr)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """CLI entry point."""
    import typer

    app = typer.Typer()

    @app.command()
    def start_cmd(
        server_ref: str | None = typer.Argument(None, help="Server reference (module:function)"),
        transport: str = typer.Option("shttp", help="Transport type (shttp or stdio)"),
        port: int = typer.Option(8081, help="Port to run on (shttp only)"),
        host: str = typer.Option("127.0.0.1", help="Host to bind to (shttp only)")
    ):
        """Start MCP server for production."""
        run_production_server(server_ref, transport, port, host)

    app()


if __name__ == "__main__":
    main()
