"""
Smithery Python CLI

Main command-line interface for the Smithery Python SDK.
"""

import sys

import typer

from .. import __version__
from ..utils.console import console
from ..utils.project import get_server_ref_from_config
from .dev import run_dev_server
from .init import create_project
from .start import run_production_server

# Create the main Typer app
app = typer.Typer(
    name="smithery",
    help="[cyan]Smithery Python SDK[/cyan] - Develop and run python MCP servers",
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        typer.echo(f"smithery {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool | None = typer.Option(
        None, "--version", callback=version_callback, help="Show version and exit"
    )
):
    """Smithery Python SDK - Develop and run MCP servers"""
    # version parameter is handled by callback
    pass


@app.command()
def init(
    project_name: str | None = typer.Argument(
        None, help="Name of the project to initialize"
    )
):
    """Initialize a new [green]Smithery Python MCP project[/green]."""
    try:
        create_project(project_name)
    except KeyboardInterrupt:
        console.warning("Operation cancelled")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to initialize project: {e}")
        sys.exit(1)


@app.command()
def dev(
    server_function: str | None = typer.Argument(
        None, help="Server function (e.g., src.server:create_server)"
    ),
    transport: str = typer.Option(
        "shttp", "--transport", help="Transport type (shttp or stdio)"
    ),
    port: int = typer.Option(8081, "--port", help="Port to run on (shttp only)"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to (shttp only)"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable auto-reload (shttp only, requires uvicorn)"),
    log_level: str = typer.Option("info", "--log-level", help="Log level (critical, error, warning, info, debug, trace)"),
):
    """Run [blue]MCP server[/blue] in development mode."""
    try:
        # Get server reference from config if not provided
        server_ref = server_function or get_server_ref_from_config()

        if reload and transport != "shttp":
            console.warning("--reload is only supported with 'shttp' transport; ignoring for stdio")
        if reload and transport == "shttp":
            console.warning(
                "Note: hot reload resets in-memory server state; stateful clients may need to reinitialize their session after a reload."
            )
        run_dev_server(server_ref, transport, port, host, reload, log_level.lower())
    except KeyboardInterrupt:
        console.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to run server: {e}")
        sys.exit(1)


@app.command()
def playground(
    server_function: str | None = typer.Argument(
        None, help="Server function (e.g., src.server:create_server)"
    ),
    port: int = typer.Option(8081, "--port", help="Port to run on"),
    reload: bool = typer.Option(False, "--reload/--no-reload", help="Enable auto-reload (requires uvicorn)"),
):
    """Run server and connect [yellow]Smithery Playground[/yellow] for testing."""
    try:
        # Import here to avoid circular imports
        import sys

        from .playground import start_playground

        if reload:
            console.warning(
                "Note: hot reload resets in-memory server state; stateful clients may need to reinitialize their session after a reload."
            )

        start_playground(server_function, port, reload)
    except KeyboardInterrupt:
        console.info("Playground stopped by user")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to start playground: {e}")
        sys.exit(1)


@app.command()
def start(
    server_function: str | None = typer.Argument(
        None, help="Server function (e.g., src.server:create_server)"
    ),
    port: int = typer.Option(8081, "--port", help="Port to run on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
):
    """Start [blue]MCP server[/blue] for production use."""
    try:
        # Use optimized production runner
        run_production_server(server_function, port, host)
    except KeyboardInterrupt:
        console.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
