"""
Smithery Python Create Command
==============================

Scaffold creation command for new Smithery Python MCP projects.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from ..utils.console import console
from .helpers import create_base_parser, handle_common_errors


def prompt_for_project_name() -> str:
    """Prompt user for project name with validation."""
    while True:
        try:
            project_name = input("What is your project name? ").strip()
            if not project_name:
                console.error("Project name cannot be empty")
                continue

            # Basic validation for valid directory name
            if any(char in project_name for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
                console.error("Project name contains invalid characters")
                continue

            return project_name
        except (KeyboardInterrupt, EOFError):
            console.warning("Operation cancelled")
            sys.exit(0)


def show_spinner(message: str, end_message: str, command_func):
    """Show a simple spinner while running a command."""
    import threading
    import time

    # Simple loading animation
    loading_chars = ["|", "/", "-", "\\"]
    loading_index = 0
    stop_loading = threading.Event()

    def spinner():
        nonlocal loading_index
        while not stop_loading.is_set():
            print(f"\r[ {loading_chars[loading_index]} ] {message}", end="", flush=True)
            loading_index = (loading_index + 1) % len(loading_chars)
            time.sleep(0.25)

    # Start spinner in background
    spinner_thread = threading.Thread(target=spinner, daemon=True)
    spinner_thread.start()

    try:
        result = command_func()
        stop_loading.set()
        spinner_thread.join(timeout=0.1)
        print(f"\r\x1b[K[ ✓ ] {end_message}")
        return result
    except Exception as e:
        stop_loading.set()
        spinner_thread.join(timeout=0.1)
        print(f"\r\x1b[K[ ✗ ] Failed: {e}")
        raise


def clone_scaffold(project_name: str) -> None:
    """Clone the scaffold repository and extract the Python scaffold."""

    def clone_and_extract():
        # Create temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            clone_path = temp_path / "smithery-sdk"

            # Clone the SDK repository
            subprocess.run([
                "git", "clone", "--depth", "1",
                "https://github.com/smithery-ai/sdk.git",
                str(clone_path)
            ], check=True, capture_output=True, text=True)

            # Path to Python scaffold
            scaffold_source = clone_path / "python" / "scaffold"

            if not scaffold_source.exists():
                raise FileNotFoundError(f"Python scaffold not found at {scaffold_source}")

            # Copy scaffold to project directory
            project_path = Path(project_name)
            if project_path.exists():
                raise FileExistsError(f"Directory '{project_name}' already exists")

            shutil.copytree(scaffold_source, project_path)

            # Remove .git directory if it exists
            git_dir = project_path / ".git"
            if git_dir.exists():
                shutil.rmtree(git_dir)

    show_spinner(
        "Cloning scaffold from GitHub...",
        "Scaffold cloned successfully",
        clone_and_extract
    )


def update_project_files(project_name: str) -> None:
    """Update project files with the actual project name."""

    def update_files():
        project_path = Path(project_name)

        # Update pyproject.toml
        pyproject_path = project_path / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()

            # Replace project name
            content = content.replace('name = "my-mcp-server"', f'name = "{project_name}"')

            # Update smithery dependency to use published version instead of local path
            content = content.replace(
                'smithery @ file:///Users/arjun/Documents/github/smithery/sdk/python',
                'smithery>=0.1.8'
            )

            pyproject_path.write_text(content)

    show_spinner(
        "Updating project configuration...",
        "Project configuration updated",
        update_files
    )


def install_dependencies(project_name: str) -> None:
    """Install project dependencies using uv."""

    def install():
        project_path = Path(project_name)

        # Check if uv is available
        try:
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as err:
            raise RuntimeError("uv is required but not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/") from err

        # Install dependencies
        subprocess.run([
            "uv", "sync"
        ], cwd=project_path, check=True, capture_output=True, text=True)

    show_spinner(
        "Installing dependencies...",
        "Dependencies installed successfully",
        install
    )


def show_success_message(project_name: str) -> None:
    """Show success message with next steps."""
    console.success("Project initialized successfully!")
    console.plain("")
    console.info("Next steps:")
    console.plain(f"  cd {project_name}")
    console.plain("  uv run smithery run")
    console.plain("")
    console.muted("Tip: Try 'Say hello to John' to exercise your tool.")


def create_project(project_name: str | None = None) -> None:
    """
    Initialize a new Smithery Python MCP project.

    Args:
        project_name: Name of the project. If None, will prompt user.
    """
    # Get project name
    if not project_name:
        project_name = prompt_for_project_name()
    else:
        print(f"Initializing project: {project_name}")

    try:
        # Clone scaffold
        clone_scaffold(project_name)

        # Update project files
        update_project_files(project_name)

        # Install dependencies
        install_dependencies(project_name)

        # Show success message
        show_success_message(project_name)

    except KeyboardInterrupt:
        console.warning("Operation cancelled")
        # Clean up partial project if it exists
        project_path = Path(project_name)
        if project_path.exists():
            try:
                shutil.rmtree(project_path)
                console.warning("Cleaned up partial project directory")
            except Exception:
                pass
        sys.exit(0)
    except Exception as e:
        console.error(f"Failed to initialize project: {e}")
        # Clean up partial project if it exists
        project_path = Path(project_name)
        if project_path.exists():
            try:
                shutil.rmtree(project_path)
                console.warning("Cleaned up partial project directory")
            except Exception:
                pass
        sys.exit(1)


@handle_common_errors
def main() -> None:
    """CLI entry point for Smithery Python init command."""
    parser = create_base_parser(
        prog="smithery init",
        description="Initialize a new Smithery Python MCP project",
        epilog="""
Examples:
  smithery init                    # Prompt for project name
  smithery init my-awesome-server  # Initialize with specific name
        """
    )

    parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the project to initialize"
    )

    args = parser.parse_args()
    create_project(args.project_name)


if __name__ == "__main__":
    main()
