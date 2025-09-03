"""
Smithery Python Build System
============================

Command-line interface for building and running Smithery Python MCP servers.
Provides build and run commands with support for multiple transports.
"""

import argparse
import inspect
import os
import sys
from collections.abc import Callable
from importlib import import_module
from typing import Any, TypedDict

from mcp.server.fastmcp import FastMCP
from rich.console import Console

# Core dependencies required by all Smithery Python projects
from pydantic import BaseModel

from ..server.fastmcp_patch import SmitheryFastMCP

# Initialize rich console
console = Console()


class SmitheryModule(TypedDict, total=False):
    """Type definition for a Smithery Python module contract."""
    create_server: Callable[[BaseModel | dict[str, Any]], SmitheryFastMCP]  # Server creation function
    config_schema: type[BaseModel] | None  # Optional Pydantic config model





def import_server_module(server_ref: str) -> SmitheryModule:
    """
    Import and validate a Smithery server module.

    Args:
        server_ref: Module reference in format 'module.path:function'

    Returns:
        SmitheryModule containing the server function and optional config schema

    Raises:
        ModuleNotFoundError: If the module cannot be imported
        AttributeError: If the specified function is not found
    """
    try:
        if ":" not in server_ref:
            raise ValueError(f"Server reference must include function name: '{server_ref}'. Expected format: 'module.path:function_name'")
        
        module_path, function_name = server_ref.split(":", 1)

        # Ensure current directory is in Python path for relative imports
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        console.print(f"[cyan][smithery][/cyan] Importing module: {module_path}")
        console.print(f"[cyan][smithery][/cyan] Looking for function: {function_name}")
        console.print(f"[cyan][smithery][/cyan] Working directory: {current_dir}")

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
                    console.print(f"[yellow]⚠ Warning: Function return type is {return_annotation.__name__ if hasattr(return_annotation, '__name__') else return_annotation}, expected SmitheryFastMCP[/yellow]")
            else:
                console.print(f"[yellow]⚠ Warning: No return type annotation found. Expected: -> SmitheryFastMCP[/yellow]")
            
            # Check parameter signature
            params = list(sig.parameters.values())
            if len(params) != 1:
                console.print(f"[yellow]⚠ Warning: Expected exactly 1 parameter (config), found {len(params)}[/yellow]")
            elif params[0].name not in ('config', 'cfg', 'configuration'):
                console.print(f"[yellow]⚠ Warning: Parameter name '{params[0].name}' should be 'config' for clarity[/yellow]")
                
        except Exception as e:
            console.print(f"[yellow]⚠ Warning: Could not validate function signature: {e}[/yellow]")

        # Get optional config schema
        config_schema = getattr(module, 'config_schema', None)

        return {
            'create_server': server_function,
            'config_schema': config_schema,
        }
    except ModuleNotFoundError as e:
        console.print(f"[red]✗ Failed to import server module '{server_ref}': {e}[/red]", file=sys.stderr)
        console.print(f"[yellow]✗ Module resolution tips:[/yellow]")
        console.print(f"  - Ensure you're running from the project root directory")
        console.print(f"  - Current working directory: {os.getcwd()}")
        console.print(f"  - Looking for module: {module_path}")
        console.print(f"  - Python path: {sys.path[:3]}...")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]✗ Failed to import server module '{server_ref}': {e}[/red]", file=sys.stderr)
        console.print(f"[yellow]✗ Expected configuration in pyproject.toml:[/yellow]")
        console.print(f"[cyan]  [tool.smithery][/cyan]")
        console.print(f"[cyan]  server = \"module.path:function_name\"[/cyan]")
        console.print(f"[yellow]✗ Expected module contract:[/yellow]")
        console.print(f"  - function_name = function(config) -> FastMCP")
        console.print(f"  - config_schema = class(BaseModel)  # Optional")
        sys.exit(1)





def build_server(server_ref: str, output_file: str = ".smithery/server.py", transport: str = "shttp") -> None:
    """
    Build a standalone server executable from a server reference.

    Args:
        server_ref: Module reference to build
        output_file: Path where the built server will be written
        transport: Transport type ('shttp' or 'stdio')
    """
    from pathlib import Path

    console.print(f"[cyan][smithery][/cyan] Building Python MCP server with {transport} transport...")
    console.print(f"[cyan][smithery][/cyan] Server reference: {server_ref}")

    # Select appropriate bootstrap template
    bootstrap_file = "shttp_bootstrap.py" if transport == "shttp" else "stdio_bootstrap.py"
    bootstrap_path = Path(__file__).parent.parent / "runtime" / bootstrap_file

    if not bootstrap_path.exists():
        raise FileNotFoundError(f"Bootstrap template not found: {bootstrap_path}")

    # Generate server content from template
    bootstrap_content = bootstrap_path.read_text()

    # Parse server reference
    module_path = server_ref.split(":")[0] if ":" in server_ref else server_ref
    function_name = server_ref.split(":")[1] if ":" in server_ref else "default"

    # Replace placeholders with actual values (like uvicorn approach)
    server_content = bootstrap_content.replace("$SMITHERY_MODULE", module_path)
    server_content = server_content.replace("$SMITHERY_FUNCTION", function_name)

    # Write output file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(server_content)

    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod(output_path, 0o755)

    console.print(f"[cyan][smithery][/cyan] Python server created: {output_file}")


def get_server_ref_from_config() -> str:
    """
    Get server reference from pyproject.toml [tool.smithery] configuration.

    Returns:
        Server reference string from [tool.smithery].server

    Raises:
        SystemExit: If configuration is missing or invalid
    """
    from pathlib import Path

    import toml

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        console.print(f"[red]✗ pyproject.toml not found. Please run from project root.[/red]", file=sys.stderr)
        sys.exit(1)

    try:
        pyproject = toml.load(pyproject_path)
    except Exception as e:
        console.print(f"[red]✗ Failed to parse pyproject.toml: {e}[/red]", file=sys.stderr)
        sys.exit(1)
    
    # Check [tool.smithery] configuration
    smithery_config = pyproject.get("tool", {}).get("smithery", {})
    server_ref = smithery_config.get("server")
    
    if not server_ref:
        console.print(f"[red]✗ Server reference not found in pyproject.toml[/red]", file=sys.stderr)
        console.print(f"[yellow]✗ Please add [tool.smithery] section with your server function:[/yellow]", file=sys.stderr)
        console.print(f"[cyan]  [tool.smithery][/cyan]", file=sys.stderr)
        console.print(f"[cyan]  server = \"src.server:your_server_function\"[/cyan]", file=sys.stderr)
        console.print(f"  # Example: server = \"src.server:create_server\"", file=sys.stderr)
        sys.exit(1)
    
    return server_ref


def main() -> None:
    """CLI entry point for Smithery Python build system."""
    parser = argparse.ArgumentParser(
        description="Build standalone MCP servers from Python modules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery build                           # Read from pyproject.toml [tool.smithery].server
  smithery build src.server:create_server  # Explicit server reference
  smithery build --transport stdio         # Build with stdio transport
        """
    )

    parser.add_argument(
        "server_ref",
        nargs="?",
        help="Server reference (module:function). Read from pyproject.toml [tool.smithery].server if not provided."
    )
    parser.add_argument(
        "-o", "--output",
        default=".smithery/server.py",
        help="Output file path"
    )
    parser.add_argument(
        "--transport",
        choices=["shttp", "stdio"],
        default="shttp",
        help="Transport type"
    )

    args = parser.parse_args()

    # Get server reference from config if not provided explicitly
    server_ref = args.server_ref or get_server_ref_from_config()

    build_server(server_ref, args.output, args.transport)


if __name__ == "__main__":
    main()
