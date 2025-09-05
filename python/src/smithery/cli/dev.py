"""
Smithery Python Run

Command-line interface for running Smithery Python MCP servers.
"""

import inspect
import sys
from collections.abc import Callable
from importlib import import_module
from typing import Any, TypedDict

from pydantic import BaseModel

from ..server.fastmcp_patch import SmitheryFastMCP
from ..utils.console import console
from ..utils.project import get_server_ref_from_config


class SmitheryModule(TypedDict, total=False):
    """Type definition for a Smithery Python module contract."""
    create_server: Callable[[BaseModel | dict[str, Any]], SmitheryFastMCP]  # Server creation function
    config_schema: type[BaseModel] | None  # Optional Pydantic config model


def import_server_module(server_ref: str) -> SmitheryModule:
    """Import and validate Smithery server module."""
    try:
        if ":" not in server_ref:
            raise ValueError(f"Server reference must include function name: '{server_ref}'. Expected format: 'module.path:function_name'")

        module_path, function_name = server_ref.split(":", 1)

        console.info(f"Importing module: {module_path}", muted=True)
        console.info(f"Looking for function: {function_name}", muted=True)

        module = import_module(module_path)

        # Get the specified server function
        if not hasattr(module, function_name):
            raise AttributeError(f"Function '{function_name}' not found in module '{module_path}'")

        server_function = getattr(module, function_name)
        if not callable(server_function):
            raise AttributeError(f"'{function_name}' is not callable in module '{module_path}'")

        # Validate function signature and return type
        try:
            sig = inspect.signature(server_function)
            return_annotation = sig.return_annotation

            # Check if return type annotation is present and correct
            if return_annotation != inspect.Signature.empty:
                if return_annotation != SmitheryFastMCP:
                    annotation_name = getattr(return_annotation, '__name__', str(return_annotation))
                    console.warning(f"Function return type is {annotation_name}, expected SmitheryFastMCP")
            else:
                console.warning("No return type annotation found. Expected: -> SmitheryFastMCP")

            # Check parameter signature
            params = list(sig.parameters.values())
            if len(params) != 1:
                console.warning(f"Expected exactly 1 parameter (config), found {len(params)}")
            elif len(params) == 1 and params[0].name not in ('config', 'cfg', 'configuration'):
                console.warning(f"Parameter name '{params[0].name}' should be 'config' for clarity")

        except Exception as e:
            console.warning(f"Could not validate function signature: {e}")

        # Get config schema - check decorator metadata first, then module-level variable
        config_schema = None

        # Priority 1: Check for decorator metadata
        if hasattr(server_function, '_smithery_config_schema'):
            config_schema = server_function._smithery_config_schema
            console.info("Using config schema from @smithery decorator", muted=True)

        # Priority 2: Fall back to module-level variable (backward compatibility)
        if not config_schema:
            config_schema = getattr(module, 'config_schema', None)
            if config_schema:
                console.info("Using config schema from module-level variable", muted=True)

        # Validate config schema if present
        if config_schema and not (inspect.isclass(config_schema) and issubclass(config_schema, BaseModel)):
            console.warning(f"config_schema should be a Pydantic BaseModel class, got {type(config_schema).__name__}")

        return {
            'create_server': server_function,
            'config_schema': config_schema,
        }
    except ModuleNotFoundError as e:
        console.error(f"Failed to import server module '{server_ref}': {e}")
        console.nested("Module resolution tips:")
        console.indented("Make sure your package is built and installed:")
        console.indented("  uv sync    # Install dependencies")
        console.indented("  uv build   # Build the package")
        console.indented("Or run in development mode:")
        console.indented("  uv run dev # Uses editable install")
        sys.exit(1)
    except Exception as e:
        console.error(f"Failed to import server module '{server_ref}': {e}")
        console.nested("Expected configuration in pyproject.toml:")
        console.indented("[tool.smithery]")
        console.indented('server = "module.path:function_name"')
        console.nested("Expected module contract:")
        console.indented("function_name = function(config) -> SmitheryFastMCP")
        console.indented("config_schema = class(BaseModel)  # Optional")
        sys.exit(1)


def run_server(server_ref: str, transport: str = "shttp", port: int = 8081, host: str = "127.0.0.1") -> None:
    """Run Smithery MCP server."""
    console.rich_console.print(f"Starting [cyan]Python MCP server[/cyan] with [yellow]{transport}[/yellow] transport...")
    console.rich_console.print(f"Server reference: [green]{server_ref}[/green]")

    try:
        # Import and validate server module
        server_module = import_server_module(server_ref)
        create_server = server_module['create_server']
        config_schema = server_module.get('config_schema')

        # Create config instance
        config: Any = {}
        if config_schema:
            try:
                config = config_schema()
                console.rich_console.print(f"Using config schema: [blue]{config_schema.__name__}[/blue]")
            except Exception as e:
                console.warning(f"Failed to instantiate config schema: {e}")
                console.warning("Proceeding with empty config")

        # Create server instance
        console.info("Creating server instance...")
        server = create_server(config)

        if transport == "shttp":
            # Set server configuration for HTTP transport
            server.settings.port = port
            server.settings.host = host

            console.rich_console.print(f"MCP server starting on [green]{host}:{port}[/green]")
            console.rich_console.print("Transport: [cyan]streamable HTTP[/cyan]")

            # Run with streamable HTTP transport
            server.run(transport="streamable-http")

        elif transport == "stdio":
            console.rich_console.print("MCP server starting with [cyan]stdio[/cyan] transport")

            # Run with stdio transport
            server.run(transport="stdio")

        else:
            raise ValueError(f"Unsupported transport: {transport}")

    except KeyboardInterrupt:
        console.info("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to start MCP server: {e}")
        sys.exit(1)


def main() -> None:
    """CLI entry point for dev command."""

    import typer

    app = typer.Typer()

    @app.command()
    def dev_cmd(
        server_ref: str | None = typer.Argument(None, help="Server reference (module:function)"),
        transport: str = typer.Option("shttp", help="Transport type (shttp or stdio)"),
        port: int = typer.Option(8081, help="Port to run on (shttp only)"),
        host: str = typer.Option("127.0.0.1", help="Host to bind to (shttp only)")
    ):
        """Run Smithery MCP servers in development mode (like uvicorn)."""
        # Get server reference from config if not provided explicitly
        server_reference = server_ref or get_server_ref_from_config()
        run_server(server_reference, transport, port, host)

    app()


if __name__ == "__main__":
    main()
