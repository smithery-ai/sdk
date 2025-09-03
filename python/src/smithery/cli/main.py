"""
Smithery CLI Main Entry Point
============================

Main command-line interface dispatcher for Smithery Python SDK.
Handles subcommands like 'build', 'dev', etc.
"""

import argparse
import sys
from typing import List, Optional

from .build import build_server, get_server_ref_from_config
from .run import run_server
from .create import create_project


def build_command(args: argparse.Namespace) -> None:
    """Handle the 'build' subcommand."""
    # Get server function from config if not provided
    server_function = args.server_function or get_server_ref_from_config()
    build_server(server_function, args.output, args.transport)


def run_command(args: argparse.Namespace) -> None:
    """Handle the 'run' subcommand."""
    # Get server function from config if not provided
    server_function = args.server_function or get_server_ref_from_config()
    run_server(server_function, args.transport, args.port, args.host)


def create_command(args: argparse.Namespace) -> None:
    """Handle the 'create' subcommand."""
    create_project(args.project_name)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="smithery",
        description="Smithery Python SDK - Build and manage MCP servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Add version argument
    parser.add_argument(
        "--version", 
        action="version", 
        version="smithery 0.1.8"
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
    
    # Create subcommand
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new Smithery Python MCP project",
        description="Scaffold a new Smithery Python MCP project with all necessary files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery create                    # Prompt for project name
  smithery create my-awesome-server  # Create with specific name
        """
    )
    
    create_parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the project to create"
    )
    create_parser.set_defaults(func=create_command)
    
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    """Main CLI entry point."""
    parser = create_parser()
    
    # If no arguments provided, show help
    if argv is None:
        argv = sys.argv[1:]
    
    if not argv:
        parser.print_help()
        return
    
    args = parser.parse_args(argv)
    
    # If no subcommand provided, show help
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    
    # Execute the subcommand
    args.func(args)


if __name__ == "__main__":
    main()
