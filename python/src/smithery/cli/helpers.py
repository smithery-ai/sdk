"""
Smithery CLI Helpers
====================

Shared utilities and helpers for Smithery CLI commands.
Consolidates common patterns like argument parsing, formatters, and configuration.
"""

import argparse
import sys
from pathlib import Path

from ..utils.console import Colors, console


class ColoredHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom colored help formatter."""

    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = f"{Colors.CYAN}usage:{Colors.RESET} "
        return super()._format_usage(usage, actions, groups, prefix)

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = f"{Colors.CYAN}usage:{Colors.RESET} "
        return super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        if heading == "positional arguments":
            heading = f"{Colors.CYAN}Commands:{Colors.RESET}"
        elif heading == "arguments":
            heading = f"{Colors.CYAN}Arguments:{Colors.RESET}"
        elif heading == "options":
            heading = f"{Colors.CYAN}Options:{Colors.RESET}"
        return super().start_section(heading)

    def _format_action(self, action):
        # Get the original formatted action
        result = super()._format_action(action)

        # Color command names (subparsers) for main CLI
        if hasattr(action, 'dest') and action.dest in ('build', 'run', 'init'):
            # Find and color the command name
            lines = result.split('\n')
            if lines:
                first_line = lines[0]
                # Color the command name at the beginning
                parts = first_line.split(None, 1)
                if len(parts) >= 2:
                    command = parts[0]
                    description = parts[1]
                    colored_line = f'  {Colors.GREEN}{command}{Colors.RESET}  {description}'
                    lines[0] = colored_line
                    result = '\n'.join(lines)

        return result


def create_base_parser(prog: str, description: str, epilog: str = "") -> argparse.ArgumentParser:
    """Create base argument parser with consistent styling."""
    return argparse.ArgumentParser(
        prog=prog,
        description=f"{Colors.GRAY}{description}{Colors.RESET}",
        formatter_class=ColoredHelpFormatter,
        epilog=epilog
    )


def get_server_ref_from_config() -> str:
    """Get server reference from pyproject.toml config."""
    import toml

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        console.error("pyproject.toml not found. Please run from project root.")
        sys.exit(1)

    try:
        pyproject = toml.load(pyproject_path)
    except Exception as e:
        console.error(f"Failed to parse pyproject.toml: {e}")
        sys.exit(1)

    # Check [tool.smithery] configuration
    smithery_config = pyproject.get("tool", {}).get("smithery", {})
    server_ref = smithery_config.get("server")

    if not server_ref:
        console.error("Server reference not found in pyproject.toml")
        console.nested("Please add [tool.smithery] section with your server function:", color=Colors.YELLOW)
        console.indented("[tool.smithery]")
        console.indented('server = "src.server:your_server_function"')
        console.indented('# Example: server = "src.server:create_server"', color=Colors.GRAY)
        sys.exit(1)

    return server_ref


def add_server_ref_argument(parser: argparse.ArgumentParser, help_text: str = None) -> None:
    """Add server reference argument to parser."""
    if help_text is None:
        help_text = "Server reference (module:function). Read from pyproject.toml [tool.smithery].server if not provided."

    parser.add_argument(
        "server_function",
        nargs="?",
        help=help_text
    )


def add_transport_argument(parser: argparse.ArgumentParser, default: str = "shttp") -> None:
    """Add transport argument to parser."""
    parser.add_argument(
        "--transport",
        choices=["shttp", "stdio"],
        default=default,
        help=f"Transport type (default: {default})"
    )


def resolve_server_ref(args: argparse.Namespace) -> str:
    """Resolve server reference from args or config."""
    return args.server_function or get_server_ref_from_config()


def handle_common_errors(func):
    """Handle common CLI errors gracefully."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            console.warning("Operation cancelled")
            sys.exit(0)
        except Exception as e:
            console.error(f"Failed to execute command: {e}")
            sys.exit(1)
    return wrapper
