"""
Smithery Python Run

Command-line interface for running Smithery Python MCP servers.
"""

import os
import sys
from collections.abc import Callable
from importlib import import_module
from typing import Any, TypedDict

from pydantic import BaseModel

from ..server.fastmcp_patch import SmitheryFastMCP
from ..utils.console import console
from ..utils.network import find_available_port


def validate_project_setup() -> str:
    """Project Discovery & Validation

    Returns: server_reference string (e.g., "my_server.server:create_server")
    Raises: SystemExit with clear error messages for each failure scenario
    """
    # Find project root and validate pyproject.toml exists
    if not os.path.exists("pyproject.toml"):
        console.error("No pyproject.toml found in current directory")
        console.nested("Make sure you're in a Python project directory")
        console.indented("Expected file: [cyan]pyproject.toml[/cyan]")
        sys.exit(1)

    # Read and parse pyproject.toml
    try:
        import tomllib
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
    except Exception as e:
        console.error(f"Failed to read pyproject.toml: {e}")
        console.nested("Ensure pyproject.toml is valid TOML format")
        sys.exit(1)

    # Extract [tool.smithery] section
    tool_config = pyproject.get("tool", {})
    smithery_config = tool_config.get("smithery", {})

    if not smithery_config:
        console.error("Missing \\[tool.smithery] configuration in pyproject.toml")
        console.nested("Add to your pyproject.toml:")
        console.indented("[cyan]\\[tool.smithery][/cyan]")
        console.indented('[cyan]server = "my_server.server:create_server"[/cyan]')
        sys.exit(1)

    # Get server reference
    server_ref = smithery_config.get("server")
    if not server_ref:
        console.error("Missing 'server' in \\[tool.smithery] configuration")
        console.nested("Add to your pyproject.toml:")
        console.indented("[cyan]\\[tool.smithery][/cyan]")
        console.indented('[cyan]server = "my_server.server:create_server"[/cyan]')
        sys.exit(1)

    # Validate server reference format
    if ":" not in server_ref:
        console.error(f"Invalid server reference format: '{server_ref}'")
        console.nested("Expected format: 'module.path:function_name'")
        console.indented("Example: 'my_server.server:create_server'")
        sys.exit(1)

    console.info("✓ Project setup validated", muted=True)
    console.rich_console.print(f"Server reference: [blue]{server_ref}[/blue]")
    return server_ref


class SmitheryModule(TypedDict, total=False):
    """Type definition for a Smithery Python module contract."""
    create_server: Callable[[BaseModel | dict[str, Any]], SmitheryFastMCP]  # Server creation function
    config_schema: type[BaseModel] | None  # Optional Pydantic config model


def import_server_module(server_ref: str) -> SmitheryModule:
    """Module Resolution & Import

    Args: server_ref like "my_server.server:create_server"
    Returns: SmitheryModule with function and optional config schema
    Raises: SystemExit with clear error messages for import failures
    """
    module_path, function_name = server_ref.split(":", 1)

    console.info(f"Importing module: {module_path}", muted=True)
    console.info(f"Looking for function: {function_name}", muted=True)

    try:
        # Import the module (assumes proper Python environment setup)
        module = import_module(module_path)

        # Check if function exists
        if not hasattr(module, function_name):
            console.error(f"Function '{function_name}' not found in module '{module_path}'")
            console.nested("Check your server module has the function specified in pyproject.toml")
            console.indented(f"Expected: def {function_name}() in {module_path}")
            sys.exit(1)

        # Get the function
        server_function = getattr(module, function_name)
        if not callable(server_function):
            console.error(f"'{function_name}' is not callable in module '{module_path}'")
            console.nested("The server reference must point to a function")
            sys.exit(1)

        # Get config schema (optional)
        config_schema = None
        if hasattr(server_function, '_smithery_config_schema'):
            config_schema = server_function._smithery_config_schema
            console.info("Using config schema from @smithery decorator", muted=True)
        elif hasattr(module, 'config_schema'):
            config_schema = module.config_schema
            console.info("Using config schema from module-level variable", muted=True)

        console.info("✓ Module imported successfully", muted=True)
        return {
            'create_server': server_function,
            'config_schema': config_schema,
        }

    except ImportError as e:
        console.error(f"Failed to import module '{module_path}': {e}")
        console.nested("Make sure your project environment is set up correctly")
        console.indented("Run: uv sync")
        console.indented("Then: uv run smithery dev")
        sys.exit(1)
    except Exception as e:
        console.error(f"Unexpected error importing module '{module_path}': {e}")
        sys.exit(1)


def create_and_run_server(
    server_module: SmitheryModule,
    transport: str = "shttp",
    port: int = 8081,
    host: str = "127.0.0.1",
    reload: bool = False,
    server_ref: str | None = None,
) -> int:
    """Server Creation & Execution

    Args: server_module from Stage 2, transport settings
    Raises: SystemExit with clear error messages for server creation/startup failures
    """
    create_server = server_module['create_server']
    config_schema = server_module.get('config_schema')

    console.info("Creating server instance...", muted=True)

    try:
        # Create config instance
        if config_schema:
            try:
                config_schema()
                console.info(f"Using config schema: {config_schema.__name__}", muted=True)
            except Exception as e:
                console.warning(f"Failed to instantiate config schema: {e}")
                console.warning("Proceeding with empty config")

        # Call user's server creation function (no config parameter needed)
        server = create_server()

        # Validate server instance
        if not hasattr(server, 'run'):
            console.error("Server function must return a FastMCP server instance")
            console.nested("Expected: return FastMCP(...)")
            sys.exit(1)

        console.rich_console.print("[green]✓ Server created successfully[/green]")

        # Configure and start server
        if transport == "shttp":
            # Find an available port, starting with the requested port
            console.info(f"Checking port availability for {host}:{port}", muted=True)
            try:
                actual_port = find_available_port(port, host)
                if actual_port != port:
                    console.warning(f"Port {port} is in use, using port {actual_port} instead")
                    port = actual_port
                else:
                    console.info(f"Port {port} is available", muted=True)
            except RuntimeError as e:
                console.error(f"Could not find an available port: {e}")
                sys.exit(1)

            if reload:
                try:
                    import uvicorn  # type: ignore
                except Exception:
                    console.error("Reload requested but 'uvicorn' is not installed")
                    console.nested("Install it in your project environment:")
                    console.indented("uv add uvicorn  # or: pip install uvicorn")
                    sys.exit(1)

                # Pass server ref for reloader to reconstruct the app in a fresh interpreter
                if server_ref:
                    os.environ["SMITHERY_SERVER_REF"] = server_ref

                console.info(f"Starting MCP server with reload on {host}:{port}")
                console.info("Transport: streamable HTTP (uvicorn --reload)", muted=True)

                # Use import string + factory so uvicorn can reload cleanly
                uvicorn.run(
                    "smithery.cli.dev:get_reloader_streamable_http_app",
                    host=host,
                    port=port,
                    reload=True,
                    factory=True,
                )
            else:
                server.settings.port = port
                server.settings.host = host

                console.info(f"Starting MCP server on {host}:{port}")
                console.info("Transport: streamable HTTP", muted=True)

                server.run(transport="streamable-http")

        elif transport == "stdio":
            console.info("Starting MCP server with stdio transport")
            server.run(transport="stdio")
            return 0  # stdio doesn't use ports

        else:
            console.error(f"Unsupported transport: {transport}")
            console.nested("Supported transports: shttp, stdio")
            sys.exit(1)

    except Exception as e:
        console.error(f"Failed to create or start server: {e}")
        console.nested("Check your server function implementation")
        sys.exit(1)

    return port  # Return the resolved port for shttp


def run_server(server_ref: str | None = None, transport: str = "shttp", port: int = 8081, host: str = "127.0.0.1", reload: bool = False) -> int:
    """Run Smithery MCP server using clean 3-stage approach.

    Returns:
        The actual port used by the server (may differ from requested port due to deconfliction)
    """
    console.rich_console.print(f"Starting [cyan]Python MCP server[/cyan] with [yellow]{transport}[/yellow] transport...")

    try:
        # Project Discovery & Validation
        if server_ref is None:
            server_ref = validate_project_setup()
        else:
            console.info(f"Using provided server reference: {server_ref}")

        # Module Resolution & Import
        server_module = import_server_module(server_ref)

        # Server Creation & Execution
        actual_port = create_and_run_server(server_module, transport, port, host, reload, server_ref)
        return actual_port

    except KeyboardInterrupt:
        console.info("\nServer stopped by user")
        sys.exit(0)


def main() -> None:
    """CLI entry point for dev command."""

    import typer

    app = typer.Typer()

    @app.command()
    def dev_cmd(
        server_ref: str | None = typer.Argument(None, help="Server reference (module:function)"),
        transport: str = typer.Option("shttp", help="Transport type (shttp or stdio)"),
        port: int = typer.Option(8081, help="Port to run on (shttp only)"),
        host: str = typer.Option("127.0.0.1", help="Host to bind to (shttp only)"),
        reload: bool = typer.Option(False, "--reload", help="Enable auto-reload (shttp only, requires uvicorn)")
    ):
        """Run Smithery MCP servers in development mode (like uvicorn)."""
        if reload and transport != "shttp":
            console.warning("--reload is only supported with 'shttp' transport; ignoring for stdio")
        if reload and transport == "shttp":
            console.warning(
                "Hot reload resets in-memory server state; stateful clients may need to reinitialize their session after a reload."
            )
        run_server(server_ref, transport, port, host, reload)

    app()


if __name__ == "__main__":
    main()

# Factory used by uvicorn --reload (import-string target)
def get_reloader_streamable_http_app():
    """Return a fresh ASGI app for streamable HTTP using env SMITHERY_SERVER_REF.

    This function is imported by Uvicorn in a fresh interpreter on reload.
    It reconstructs the server from the configured server reference and returns
    a new ASGI application callable.
    """
    server_ref = os.environ.get("SMITHERY_SERVER_REF")
    if not server_ref:
        raise RuntimeError("SMITHERY_SERVER_REF not set for reloader")

    # Resolve and import
    server_module = import_server_module(server_ref)
    create_server = server_module['create_server']
    server = create_server()
    return server.streamable_http_app()
