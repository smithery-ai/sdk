"""
Streamlined CLI console utilities using Rich.

Features:
- Rich text formatting and colors
- Professional spinners and progress
- Clean API for common CLI patterns
- Cross-platform compatibility
"""

import sys
from contextlib import contextmanager
from typing import TextIO

from rich.console import Console as RichConsole
from rich.live import Live
from rich.spinner import Spinner


class Console:
    """Streamlined console using Rich for better output."""

    def __init__(self, file: TextIO = sys.stdout, stderr: TextIO = sys.stderr):
        self.rich_console = RichConsole(file=file, stderr=stderr)

    def success(self, message: str) -> None:
        """Print a success message."""
        self.rich_console.print(message, style="green")

    def error(self, message: str) -> None:
        """Print an error message with error icon."""
        error_console = RichConsole(stderr=True)
        error_console.print(f"✗ {message}", style="red")

    def warning(self, message: str) -> None:
        """Print a warning message."""
        self.rich_console.print(message, style="yellow")

    def info(self, message: str, muted: bool = False) -> None:
        """Print an info message."""
        if muted:
            self.rich_console.print(message, style="dim")
        else:
            self.rich_console.print(message)

    def nested(self, message: str, indent: int = 1, color: str | None = None) -> None:
        """Print a nested message (for error details)."""
        spaces = "  " * indent
        style = color if color else "dim"
        error_console = RichConsole(stderr=True)
        error_console.print(f"{spaces}↳ {message}", style=style)

    def indented(self, message: str, indent: int = 2, color: str | None = None) -> None:
        """Print an indented message without arrow."""
        spaces = "  " * indent
        style = color if color else None
        error_console = RichConsole(stderr=True)
        error_console.print(f"{spaces}{message}", style=style)

    def plain(self, message: str) -> None:
        """Print a plain message without styling."""
        self.rich_console.print(message)

    @contextmanager
    def spinner(self, message: str, success_message: str | None = None):
        """Context manager for showing a spinner during long operations."""
        spinner = Spinner("dots", text=message)

        with Live(spinner, console=self.rich_console, refresh_per_second=10):
            try:
                yield
                # Success - spinner will stop automatically when context exits
            except Exception:
                # Error case - spinner stops, we show error
                raise

        # Show success message after spinner stops
        if success_message:
            self.success(success_message)


# Global console instance
console = Console()


def format_error_tree(error: Exception, context: str | None = None) -> str:
    """Format an error with nested context."""
    lines = []

    # Main error
    if context:
        lines.append(f"✗ {context}")
    else:
        lines.append(f"✗ {str(error)}")

    # Add nested details if available
    if hasattr(error, '__cause__') and error.__cause__:
        lines.append(f"  ↳ {error.__cause__}")

    if hasattr(error, '__context__') and error.__context__ and error.__context__ != error.__cause__:
        lines.append(f"  ↳ {error.__context__}")

    return "\n".join(lines)


# Convenience functions for common patterns
def success(message: str) -> None:
    """Quick success message."""
    console.success(message)


def error(message: str) -> None:
    """Quick error message."""
    console.error(message)


def warning(message: str) -> None:
    """Quick warning message."""
    console.warning(message)


def info(message: str, muted: bool = False) -> None:
    """Quick info message."""
    console.info(message, muted=muted)


def muted(message: str) -> None:
    """Quick muted message for less important info."""
    console.info(message, muted=True)
