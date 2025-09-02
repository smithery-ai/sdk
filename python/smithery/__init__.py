"""
Smithery Python SDK
==================

SDK for using Smithery in Python.
"""

from .url import create_smithery_url
from .server.stateful import (
    create_stateful_server,
    StatefulServerOptions,
    get_request_config,
    get_config_value,
    get_session_config,
    get_current_session_id,
    cleanup_session,
)
from .server.stateless import (
    create_stateless_server,
    StatelessServerOptions,
)
from .server.patched_fastmcp import (
    PatchedFastMCP,
    get_session_config as get_patched_session_config,
    cleanup_session_config,
)

__version__ = "0.1.0"

__all__ = [
    "create_smithery_url",
    "create_stateful_server",
    "StatefulServerOptions",
    "get_request_config",
    "get_config_value",
    "get_session_config",
    "get_current_session_id",
    "cleanup_session",
    "create_stateless_server",
    "StatelessServerOptions",
    "PatchedFastMCP",
    "get_patched_session_config",
    "cleanup_session_config",
]
