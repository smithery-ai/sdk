"""
Smithery CLI Main Entry Point
============================

Main command-line interface dispatcher for Smithery Python SDK.
Handles subcommands like 'build', 'dev', etc.
"""

import argparse
import sys

from ..utils.console import Colors, console
from .build import build_server
from .helpers import ColoredHelpFormatter, resolve_server_ref
from .init import create_project
from .run import run_server


def build_command(args: argparse.Namespace) -> None:
    """Handle the 'build' subcommand."""
    server_function = resolve_server_ref(args)
    build_server(server_function, args.output, args.transport)


def run_command(args: argparse.Namespace) -> None:
    """Handle the 'run' subcommand."""
    server_function = resolve_server_ref(args)
    run_server(server_function, args.transport, args.port, args.host)


def init_command(args: argparse.Namespace) -> None:
    """Handle the 'init' subcommand."""
    create_project(args.project_name)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="smithery",
        description=f"{Colors.GRAY}Smithery Python SDK - Build and manage MCP servers{Colors.RESET}",
        formatter_class=ColoredHelpFormatter,
    )

    # Add version argument
    parser.add_argument(
        "--version",
        action="version",
        version="smithery 0.1.9"
    )

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )

    # Build subcommand
    build_parser = subparsers.add_parser(
        "build",
        help="Build standalone MCP server from Python module",
        description="Build a standalone MCP server executable from your Python module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery build                           # Read from pyproject.toml [tool.smithery].server
  smithery build src.server:create_server  # Specify your server function
  smithery build --transport stdio         # Build with stdio transport
        """
    )

    build_parser.add_argument(
        "server_function",
        nargs="?",
        help="Path to your server function (e.g., src.server:create_server). Read from pyproject.toml [tool.smithery].server if not provided."
    )
    build_parser.add_argument(
        "-o", "--output",
        default=".smithery/server.py",
        help="Output file path (default: .smithery/server.py)"
    )
    build_parser.add_argument(
        "--transport",
        choices=["shttp", "stdio"],
        default="shttp",
        help="Transport type (default: shttp)"
    )
    build_parser.set_defaults(func=build_command)

    # Run subcommand
    run_parser = subparsers.add_parser(
        "run",
        help="Run MCP server directly (like uvicorn)",
        description="Run a Smithery MCP server directly without building",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery run                          # Read from pyproject.toml [tool.smithery].server
  smithery run src.server:create_server # Run specific server function
  smithery run --transport stdio        # Run with stdio transport
  smithery run --port 3000              # Run on custom port (shttp only)
        """
    )

    run_parser.add_argument(
        "server_function",
        nargs="?",
        help="Path to your server function (e.g., src.server:create_server). Read from pyproject.toml [tool.smithery].server if not provided."
    )
    run_parser.add_argument(
        "--transport",
        choices=["shttp", "stdio"],
        default="shttp",
        help="Transport type (default: shttp)"
    )
    run_parser.add_argument(
        "--port",
        type=int,
        default=8081,
        help="Port to run on (shttp only, default: 8081)"
    )
    run_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (shttp only, default: 127.0.0.1)"
    )
    run_parser.set_defaults(func=run_command)

    # Init subcommand
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new Smithery Python MCP project",
        description="Scaffold a new Smithery Python MCP project with all necessary files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery init                    # Prompt for project name
  smithery init my-awesome-server  # Initialize with specific name
        """
    )

    init_parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the project to initialize"
    )
    init_parser.set_defaults(func=init_command)

    return parser


def print_colored_help():
    """Print colored help message when no command is provided."""
    console.plain(f"{Colors.CYAN}usage:{Colors.RESET} smithery [OPTIONS] <COMMAND>")
    console.plain("")
    console.plain(f"{Colors.GRAY}Smithery Python SDK - Build and manage MCP servers{Colors.RESET}")
    console.plain("")
    console.plain(f"{Colors.CYAN}Commands:{Colors.RESET}")
    console.plain(f"  {Colors.GREEN}build{Colors.RESET}   Build standalone MCP server from Python module")
    console.plain(f"  {Colors.GREEN}run{Colors.RESET}     Run MCP server directly (like uvicorn)")
    console.plain(f"  {Colors.GREEN}init{Colors.RESET}   Initialize a new Smithery Python MCP project")
    console.plain("")
    console.plain(f"{Colors.CYAN}Options:{Colors.RESET}")
    console.plain(f"  {Colors.GRAY}-h, --help{Colors.RESET}     Show this help message and exit")
    console.plain(f"  {Colors.GRAY}--version{Colors.RESET}      Show program's version number and exit")


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point."""
    parser = create_parser()

    # If no arguments provided, show colored help
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print_colored_help()
        return

    args = parser.parse_args(argv)

    # If no subcommand provided, show colored help
    if not hasattr(args, 'func'):
        print_colored_help()
        return

    # Execute the subcommand
    args.func(args)


if __name__ == "__main__":
    main()
