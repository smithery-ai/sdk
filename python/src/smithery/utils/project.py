"""Project configuration utilities for Smithery."""

import sys
from pathlib import Path

from .console import console


def get_server_ref_from_config() -> str:
    """Get server reference from pyproject.toml config."""
    import tomllib

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        console.error("pyproject.toml not found. Please run from project root.")
        sys.exit(1)

    try:
        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)
    except Exception as e:
        console.error(f"Failed to parse pyproject.toml: {e}")
        sys.exit(1)

    # Check [tool.smithery] configuration
    smithery_config = pyproject.get("tool", {}).get("smithery", {})
    server_ref = smithery_config.get("server")

    if not server_ref:
        console.error("Server reference not found in pyproject.toml")
        console.nested("Please add [tool.smithery] section with your server function:", color="yellow")
        console.indented("[tool.smithery]")
        console.indented('server = "src.server:your_server_function"')
        console.indented('# Example: server = "src.server:create_server"', color="dim")
        sys.exit(1)

    return server_ref


def get_smithery_config() -> dict:
    """Get complete [tool.smithery] configuration from pyproject.toml."""
    import tomllib

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        console.error("pyproject.toml not found. Please run from project root.")
        sys.exit(1)

    try:
        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)
    except Exception as e:
        console.error(f"Failed to parse pyproject.toml: {e}")
        sys.exit(1)

    # Return [tool.smithery] configuration
    return pyproject.get("tool", {}).get("smithery", {})
