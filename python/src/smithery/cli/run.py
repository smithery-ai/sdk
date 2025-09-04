"""
Smithery Python Run System
===========================

Command-line interface for running Smithery Python MCP servers.
"""

import inspect
import os
import sys
from collections.abc import Callable
from importlib import import_module
from typing import Any, TypedDict

from pydantic import BaseModel

from ..server.fastmcp_patch import SmitheryFastMCP
from ..utils.console import console
from .helpers import get_server_ref_from_config


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

        # Ensure current directory is in Python path for relative imports
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        console.info(f"Importing module: {module_path}", muted=True)
        console.info(f"Looking for function: {function_name}", muted=True)
        console.info(f"Working directory: {current_dir}", muted=True)

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
                    console.warning(f"Function return type is {return_annotation.__name__ if hasattr(return_annotation, '__name__') else return_annotation}, expected SmitheryFastMCP")
            else:
                console.warning("No return type annotation found. Expected: -> SmitheryFastMCP")

            # Check parameter signature
            params = list(sig.parameters.values())
            if len(params) != 1:
                console.warning(f"Expected exactly 1 parameter (config), found {len(params)}")
            elif params[0].name not in ('config', 'cfg', 'configuration'):
                console.warning(f"Parameter name '{params[0].name}' should be 'config' for clarity")

        except Exception as e:
            console.warning(f"Could not validate function signature: {e}")

        # Get optional config schema
        config_schema = getattr(module, 'config_schema', None)

        return {
            'create_server': server_function,
            'config_schema': config_schema,
        }
    except ModuleNotFoundError as e:
        console.error(f"Failed to import server module '{server_ref}': {e}")
        console.nested("Module resolution tips:")
        console.indented("Ensure you're running from the project root directory")
        console.indented(f"Current working directory: {os.getcwd()}")
        console.indented(f"Looking for module: {module_path}")
        console.indented(f"Python path: {sys.path[:3]}...")
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
    """Run Smithery MCP server directly."""
    console.info(f"Starting Python MCP server with {transport} transport...")
    console.info(f"Server reference: {server_ref}")

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
                console.info(f"Using config schema: {config_schema.__name__}")
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

            console.info(f"MCP server starting on {host}:{port}")
            console.info("Transport: streamable HTTP")

            # Run with streamable HTTP transport
            server.run(transport="streamable-http")

        elif transport == "stdio":
            console.info("MCP server starting with stdio transport")

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
    """CLI entry point for run command."""

    import typer

    app = typer.Typer()

    @app.command()
    def run_cmd(
        server_ref: str | None = typer.Argument(None, help="Server reference (module:function)"),
        transport: str = typer.Option("shttp", help="Transport type (shttp or stdio)"),
        port: int = typer.Option(8081, help="Port to run on (shttp only)"),
        host: str = typer.Option("127.0.0.1", help="Host to bind to (shttp only)")
    ):
        """Run Smithery MCP servers directly (like uvicorn)."""
        # Get server reference from config if not provided explicitly
        server_reference = server_ref or get_server_ref_from_config()
        run_server(server_reference, transport, port, host)

    app()


if __name__ == "__main__":
    main()
