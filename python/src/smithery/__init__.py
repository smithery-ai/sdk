"""
Smithery Python SDK and CLI
"""

from .server.fastmcp_patch import (
    from_fastmcp,
)
from .utils.url import create_smithery_url

__version__ = "0.1.21"

__all__ = [
    "create_smithery_url",
    "from_fastmcp",
]
