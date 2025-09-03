"""
Smithery CLI Main Entry Point
============================

Main command-line interface dispatcher for Smithery Python SDK.
Handles subcommands like 'build', 'dev', etc.
"""

import argparse
import sys
from typing import List, Optional

from .build import build_server, auto_detect_server_ref


def build_command(args: argparse.Namespace) -> None:
    """Handle the 'build' subcommand."""
    # Auto-detect server reference if not provided
    server_ref = args.server_ref or auto_detect_server_ref()
    build_server(server_ref, args.output, args.transport)


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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smithery build                           # Auto-detect from pyproject.toml
  smithery build src.server:create_server  # Explicit server reference  
  smithery build --transport stdio         # Build with stdio transport
        """
    )
    
    build_parser.add_argument(
        "server_ref",
        nargs="?",
        help="Server reference (module:function). Auto-detected from pyproject.toml if not provided."
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
    
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # If no subcommand provided, default to build for backwards compatibility
    if not hasattr(args, 'func'):
        # Treat all arguments as if they were passed to build subcommand
        # This maintains backwards compatibility with `smithery` (no subcommand)
        build_args = argparse.Namespace(
            server_ref=getattr(args, 'server_ref', None),
            output=".smithery/server.py",
            transport="shttp"
        )
        build_command(build_args)
        return
    
    # Execute the subcommand
    args.func(args)


if __name__ == "__main__":
    main()
