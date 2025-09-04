"""
Lightweight CLI console utilities following uv's design principles.

Features:
- Unicode icons for semantic meaning
- ANSI colors with colorama shim for Windows
- Tree-structured error messages
- Smooth Braille dot spinners
- No heavy dependencies (no Rich, tqdm, etc.)
"""

import sys
import time
import threading
from typing import Optional, TextIO, Callable, Any
from contextlib import contextmanager

# Try to import colorama for Windows ANSI support
try:
    import colorama
    colorama.init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False


class Colors:
    """ANSI color codes following uv's color scheme."""
    # Reset
    RESET = "\x1b[0m"
    
    # Colors
    RED = "\x1b[31m"        # Errors
    GREEN = "\x1b[32m"      # Success
    YELLOW = "\x1b[33m"     # Warnings
    CYAN = "\x1b[36m"       # Info/brand
    GRAY = "\x1b[90m"       # Muted text
    
    # Bright variants
    BRIGHT_RED = "\x1b[91m"
    BRIGHT_GREEN = "\x1b[92m"
    BRIGHT_CYAN = "\x1b[96m"


class Icons:
    """Unicode icons following uv's semantic approach."""
    SUCCESS = "✓"           # Success operations
    ERROR = "×"             # Failure operations  
    WARNING = "⚠"           # Warning messages
    INFO = "▶"              # Progress/info
    NESTED = "↳"            # Nested causes/details
    
    # Braille spinner patterns (smooth animation)
    SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class Console:
    """Lightweight console for CLI output following uv's design."""
    
    def __init__(self, file: TextIO = sys.stdout, stderr: TextIO = sys.stderr):
        self.file = file
        self.stderr = stderr
        self._use_colors = self._should_use_colors()
    
    def _should_use_colors(self) -> bool:
        """Determine if we should use colors based on terminal capabilities."""
        # Check if stdout is a TTY and TERM is set
        if not hasattr(self.file, 'isatty') or not self.file.isatty():
            return False
        
        # Check NO_COLOR environment variable
        import os
        if os.environ.get('NO_COLOR'):
            return False
            
        # Check FORCE_COLOR environment variable
        if os.environ.get('FORCE_COLOR'):
            return True
            
        return True
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self._use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"
    
    def success(self, message: str) -> None:
        """Print a success message - clean, no prefix for normal operations."""
        colored_message = self._colorize(message, Colors.GREEN)
        print(colored_message, file=self.file)
    
    def error(self, message: str) -> None:
        """Print an error message with error icon."""
        icon = self._colorize(Icons.ERROR, Colors.RED)
        print(f"{icon} {message}", file=self.stderr)
    
    def warning(self, message: str) -> None:
        """Print a warning message."""
        # uv style: just the message, maybe in yellow for warnings
        colored_message = self._colorize(message, Colors.YELLOW)
        print(colored_message, file=self.file)
    
    def info(self, message: str, muted: bool = False) -> None:
        """Print an info message."""
        if muted:
            # Use grey for less important information
            colored_message = self._colorize(message, Colors.GRAY)
            print(colored_message, file=self.file)
        else:
            print(message, file=self.file)
    
    def nested(self, message: str, indent: int = 1, color: Optional[str] = None) -> None:
        """Print a nested message (for error details)."""
        icon = self._colorize(Icons.NESTED, Colors.GRAY)
        spaces = "  " * indent
        if color:
            message = self._colorize(message, color)
        print(f"{spaces}{icon} {message}", file=self.stderr)
    
    def indented(self, message: str, indent: int = 2, color: Optional[str] = None) -> None:
        """Print an indented message without arrow (for nested content)."""
        spaces = "  " * indent
        if color:
            message = self._colorize(message, color)
        print(f"{spaces}{message}", file=self.stderr)
    
    def plain(self, message: str) -> None:
        """Print a plain message without icons."""
        print(message, file=self.file)
    
    @contextmanager
    def spinner(self, message: str, success_message: Optional[str] = None):
        """Context manager for showing a spinner during long operations."""
        if not self._use_colors or not hasattr(self.file, 'isatty') or not self.file.isatty():
            # Fallback for non-TTY environments
            print(f"▶ {message}...", file=self.file, flush=True)
            try:
                yield
                if success_message:
                    self.success(success_message)
            except Exception:
                self.error("Operation failed")
                raise
            return
        
        # TTY spinner implementation
        stop_event = threading.Event()
        spinner_thread = None
        
        def spin():
            i = 0
            while not stop_event.is_set():
                frame = Icons.SPINNER[i % len(Icons.SPINNER)]
                colored_frame = self._colorize(frame, Colors.CYAN)
                print(f"\r{colored_frame} {message}...", end="", flush=True, file=self.file)
                time.sleep(0.1)
                i += 1
        
        try:
            spinner_thread = threading.Thread(target=spin, daemon=True)
            spinner_thread.start()
            
            yield
            
            # Success
            stop_event.set()
            if spinner_thread:
                spinner_thread.join(timeout=0.1)
            
            # Clear line and show success
            print(f"\r\x1b[K", end="", file=self.file)
            if success_message:
                self.success(success_message)
            
        except Exception as e:
            # Error
            stop_event.set()
            if spinner_thread:
                spinner_thread.join(timeout=0.1)
            
            # Clear line and show error
            print(f"\r\x1b[K", end="", file=self.file)
            self.error(f"Operation failed: {e}")
            raise


# Global console instance
console = Console()


def format_error_tree(error: Exception, context: Optional[str] = None) -> str:
    """Format an error with nested context following uv's tree structure."""
    lines = []
    
    # Main error
    icon = console._colorize(Icons.ERROR, Colors.RED)
    if context:
        lines.append(f"{icon} {context}")
    else:
        lines.append(f"{icon} {str(error)}")
    
    # Add nested details if available
    if hasattr(error, '__cause__') and error.__cause__:
        nested_icon = console._colorize(Icons.NESTED, Colors.GRAY)
        lines.append(f"  {nested_icon} {error.__cause__}")
    
    if hasattr(error, '__context__') and error.__context__ and error.__context__ != error.__cause__:
        nested_icon = console._colorize(Icons.NESTED, Colors.GRAY)
        lines.append(f"  {nested_icon} {error.__context__}")
    
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
