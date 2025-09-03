"""
Smithery Build System
====================

Build command for Smithery Python servers.
"""

import argparse
import os
import sys
from importlib import import_module
from typing import Any, Callable, Dict, Optional, Type, TypedDict, Union

# Required imports - these should always be available in a Smithery project
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from .server.fastmcp_patch import _FastMCPWrapper

# Type alias for the server type
ServerType = _FastMCPWrapper


class SmitheryModule(TypedDict, total=False):
    """Type definition for a Smithery Python module contract."""
    default: Callable[[Union[BaseModel, Dict[str, Any]]], ServerType]  # Required: function that takes config and creates server
    config_schema: Optional[Type[BaseModel]]  # Optional: Pydantic config model


def import_server_module(server_ref: str) -> SmitheryModule:
    """Import the server module and extract components."""
    try:
        # Extract module path, ignore function name (always use 'default')
        module_path = server_ref.split(":")[0] if ":" in server_ref else server_ref
        module = import_module(module_path)
        
        # Require default export (like TypeScript)
        if not hasattr(module, 'default') or not callable(getattr(module, 'default')):
            raise AttributeError("Module must export 'default' function")
        
        default_fn = getattr(module, 'default')
        config_schema = getattr(module, 'config_schema', None)
        
        print(f"[smithery] Setting up server")
        if config_schema and issubclass(config_schema, BaseModel):
            print(f"[smithery] Using config schema: {config_schema.__name__}")
        
        return {
            'default': default_fn,
            'config_schema': config_schema,
        }
    except Exception as e:
        print(f"✗ Failed to import server module '{server_ref}': {e}", file=sys.stderr)
        print("✗ Expected module contract:")
        print("  - default = function(config) -> FastMCP  # Required")
        print("  - config_schema = class(BaseModel)  # Optional")
        sys.exit(1)


def run_server(server_ref: str, transport: str = "shttp") -> None:
    """Run the server with the specified transport."""
    print(f"[smithery] Starting Python MCP server...")
    print(f"[smithery] Loading server from: {server_ref}")
    
    # Import server components
    components = import_server_module(server_ref)
    default_fn = components['default']
    config_schema = components['config_schema']
    
    # Create config instance
    config = {}
    if config_schema:
        config = config_schema()
    
    # Create server instance
    server = default_fn(config)
    
    if transport == "shttp":
        # Get port from environment or default
        port = int(os.environ.get("PORT", "8081"))
        server.settings.port = port
        print(f"✓ [smithery] MCP server starting on port {port}")
        server.run(transport="streamable-http")
    else:
        # STDIO transport
        server.run(transport="stdio")


def build_server(server_ref: str, output_file: str = ".smithery/server.py", transport: str = "shttp") -> None:
    """Build a standalone server file by injecting server reference into bootstrap."""
    from pathlib import Path
    import os
    
    print(f"[smithery] Building Python MCP server with {transport} transport...")
    print(f"[smithery] Server reference: {server_ref}")
    
    # Get the bootstrap template
    bootstrap_file = "shttp_bootstrap.py" if transport == "shttp" else "stdio_bootstrap.py"
    bootstrap_path = Path(__file__).parent.parent / "runtime" / bootstrap_file
    
    if not bootstrap_path.exists():
        raise FileNotFoundError(f"Bootstrap template not found: {bootstrap_path}")
    
    # Read bootstrap template
    bootstrap_content = bootstrap_path.read_text()
    
    # Inject server reference
    server_content = bootstrap_content.replace("SMITHERY_SERVER_REF", server_ref)
    
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the server file
    output_path.write_text(server_content)
    
    # Make it executable on Unix systems
    if os.name != 'nt':  # Not Windows
        os.chmod(output_path, 0o755)
    
    print(f"✓ [smithery] Python server created: {output_file}")


def auto_detect_server_ref() -> str:
    """Auto-detect server reference from pyproject.toml."""
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
        raise RuntimeError(f"Failed to parse pyproject.toml: {e}")


def main() -> None:
    """CLI entry point for smithery commands."""
    parser = argparse.ArgumentParser(description="Smithery Python MCP server tools")
    parser.add_argument("command", nargs="?", default="build", choices=["build", "run"], help="Command to run (default: build)")
    parser.add_argument("server_ref", nargs="?", help="Server reference (module:function). Auto-detected from pyproject.toml if not provided.")
    parser.add_argument("-o", "--output", default=".smithery/server.py", help="Output file path (build only)")
    parser.add_argument("--transport", choices=["shttp", "stdio"], default="shttp", help="Transport type")
    
    args = parser.parse_args()
    
    # Auto-detect server reference if not provided
    server_ref = args.server_ref or auto_detect_server_ref()
    
    if args.command == "build":
        build_server(server_ref, args.output, args.transport)
    elif args.command == "run":
        run_server(server_ref, args.transport)


if __name__ == "__main__":
    main()
