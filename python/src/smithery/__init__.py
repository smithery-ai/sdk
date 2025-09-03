"""
Smithery Python SDK
==================

SDK for using Smithery in Python.
"""

from .server.fastmcp_patch import (
    from_fastmcp,
)
from .utils.url import create_smithery_url
from .cli.build import run_server

__version__ = "0.1.4"

__all__ = [
    "create_smithery_url",
    "from_fastmcp",
    "run_server",
]
