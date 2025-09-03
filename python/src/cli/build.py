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

# Core dependencies required by all Smithery Python projects
from pydantic import BaseModel

from ..server.fastmcp_patch import _FastMCPWrapper

# Type alias for enhanced FastMCP server
ServerType = _FastMCPWrapper


class SmitheryModule(TypedDict, total=False):
    """Type definition for a Smithery Python module contract."""
    default: Callable[[BaseModel | dict[str, Any]], ServerType]  # Server factory function
    config_schema: type[BaseModel] | None  # Optional Pydantic config model


def _auto_detect_server_function(module) -> Callable | None:
    """
    Auto-detect server function by analyzing return type annotations.

    Looks for functions that return FastMCP or ServerType.
    Returns the first match if multiple candidates are found.
    """
    candidates = []

    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith('_'):
            continue

        try:
            sig = inspect.signature(obj)
            return_annotation = sig.return_annotation

            if return_annotation == FastMCP or return_annotation == ServerType:
                candidates.append((name, obj))
                print(f"[smithery] Found function returning FastMCP: {name}")
        except Exception:
            continue

    if len(candidates) == 1:
        name, func = candidates[0]
        print(f"[smithery] Auto-detected server function: {name}")
        return func
    elif len(candidates) > 1:
        print(f"[smithery] Multiple FastMCP functions found: {[name for name, _ in candidates]}")
        print(f"[smithery] Using first match: {candidates[0][0]}")
        return candidates[0][1]

    return None


def import_server_module(server_ref: str) -> SmitheryModule:
    """
    Import and validate a Smithery server module.

    Args:
        server_ref: Module reference in format 'module.path' or 'module.path:function'

    Returns:
        SmitheryModule containing the server function and optional config schema

    Raises:
        ModuleNotFoundError: If the module cannot be imported
        AttributeError: If no valid server function is found
    """
    try:
        module_path = server_ref.split(":")[0] if ":" in server_ref else server_ref

        # Ensure current directory is in Python path for relative imports
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        print(f"[smithery] Importing module: {module_path}")
        print(f"[smithery] Working directory: {current_dir}")

        module = import_module(module_path)

        # Locate the server function
        default_fn = None
        config_schema = getattr(module, 'config_schema', None)

        # Try explicit 'default' export first (matches TypeScript convention)
        if hasattr(module, 'default') and callable(module.default):
            default_fn = module.default
            print("[smithery] Found explicit 'default' function")

        # Fallback to auto-detection by function signature
        if default_fn is None:
            default_fn = _auto_detect_server_function(module)

        if default_fn is None:
            raise AttributeError("No valid server function found")

        print("[smithery] Setting up server")
        if config_schema and issubclass(config_schema, BaseModel):
            print(f"[smithery] Using config schema: {config_schema.__name__}")

        return {
            'default': default_fn,
            'config_schema': config_schema,
        }
    except ModuleNotFoundError as e:
        print(f"✗ Failed to import server module '{server_ref}': {e}", file=sys.stderr)
        print("✗ Module resolution tips:")
        print("  - Ensure you're running from the project root directory")
        print(f"  - Current working directory: {os.getcwd()}")
        print(f"  - Looking for module: {module_path}")
        print(f"  - Python path: {sys.path[:3]}...")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Failed to import server module '{server_ref}': {e}", file=sys.stderr)
        print("✗ Expected module contract:")
        print("  - default = function(config) -> FastMCP  # Explicit export (matches TypeScript)")
        print("  - OR any function returning FastMCP type")
        print("  - config_schema = class(BaseModel)  # Optional")
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

    print(f"[smithery] Building Python MCP server with {transport} transport...")
    print(f"[smithery] Server reference: {server_ref}")

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

    print(f"✓ [smithery] Python server created: {output_file}")


def auto_detect_server_ref() -> str:
    """
    Auto-detect server reference from pyproject.toml configuration.

    Looks for the 'server' entry in [project.scripts] section.

    Returns:
        Server reference string

    Raises:
        FileNotFoundError: If pyproject.toml is not found
        RuntimeError: If server reference cannot be determined
    """
    from pathlib import Path

    import toml

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found. Please run from project root.")

    try:
        pyproject = toml.load(pyproject_path)
        server_ref = pyproject.get("project", {}).get("scripts", {}).get("server")
        if not server_ref:
            raise KeyError("No 'server' entry found in [project.scripts]")
        return server_ref
    except Exception as e:
        raise RuntimeError(f"Failed to parse pyproject.toml: {e}") from e


def main() -> None:
    """CLI entry point for Smithery Python build system."""
    parser = argparse.ArgumentParser(
        description="Build standalone MCP servers from Python modules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery build                           # Auto-detect from pyproject.toml
  smithery build src.server:create_server  # Explicit server reference
  smithery build --transport stdio         # Build with stdio transport
        """
    )

    parser.add_argument(
        "server_ref",
        nargs="?",
        help="Server reference (module:function). Auto-detected from pyproject.toml if not provided."
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

    # Auto-detect server reference if not provided
    server_ref = args.server_ref or auto_detect_server_ref()

    build_server(server_ref, args.output, args.transport)


if __name__ == "__main__":
    main()
