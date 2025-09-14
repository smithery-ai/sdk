"""
Smithery Python SDK and CLI
"""

__version__ = "0.1.25"

# Lazy imports to avoid loading heavy dependencies for CLI tools
def __getattr__(name):
    if name == "from_fastmcp":
        from .server.fastmcp_patch import from_fastmcp
        return from_fastmcp
    elif name == "create_smithery_url":
        from .utils.url import create_smithery_url
        return create_smithery_url
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "create_smithery_url",
    "from_fastmcp",
]
