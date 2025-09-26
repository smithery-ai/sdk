"""
Smithery FastMCP Patch - Session Config Support

This provides a wrapper for FastMCP that adds middleware for smithery session config and CORS
"""

import functools
import importlib.util
import logging
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel  # type: ignore
from starlette.middleware.cors import CORSMiddleware  # type: ignore

from .middleware import SessionConfigMiddleware

if TYPE_CHECKING:
    pass

# Import both Context classes using proper spec checking
_CONTEXT_CLASSES = []

# Check for MCP SDK FastMCP Context
try:
    if importlib.util.find_spec("mcp.server.fastmcp"):
        from mcp.server.fastmcp import Context as MCPSDKContext  # type: ignore
        from mcp.server.fastmcp import FastMCP as MCPSDKFastMCP  # type: ignore
        _CONTEXT_CLASSES.append(("mcp_sdk", MCPSDKContext))
    else:
        MCPSDKContext = None
        MCPSDKFastMCP = None
except (ImportError, ModuleNotFoundError):
    MCPSDKContext = None
    MCPSDKFastMCP = None

# Check for standalone FastMCP Context
try:
    if importlib.util.find_spec("fastmcp"):
        from fastmcp import Context as FastMCPContext  # type: ignore
        from fastmcp import FastMCP as FastMCPServer  # type: ignore
        _CONTEXT_CLASSES.append(("standalone", FastMCPContext))
    else:
        FastMCPContext = None
        FastMCPServer = None
except (ImportError, ModuleNotFoundError):
    FastMCPContext = None
    FastMCPServer = None

# Determine which FastMCP to use for the function signature
FastMCP = MCPSDKFastMCP or FastMCPServer

if not FastMCP:
    raise ImportError(
        "Neither MCP SDK FastMCP nor standalone FastMCP is available. "
    )

# Log which FastMCP flavor is being used
logger = logging.getLogger(__name__)
if MCPSDKFastMCP:
    logger.debug("Using MCP SDK FastMCP implementation")
elif FastMCPServer:
    logger.debug("Using standalone FastMCP implementation")


def ensure_context_patched() -> None:
    """Add session_config property to all available FastMCP Context classes (idempotent)."""

    # Module-level flag for one-time warning
    _session_config_warned = False

    @property
    def session_config(self) -> dict[str, Any]:
        """Get session config from request scope."""
        nonlocal _session_config_warned
        try:
            if hasattr(self, 'request_context') and hasattr(self.request_context, "request") and hasattr(self.request_context.request, "scope"):
                scope = self.request_context.request.scope
                config = scope.get("session_config")
                if config is not None:
                    return config
        except (AttributeError, KeyError):
            pass

        # Log warning once when falling back to empty dict
        if not _session_config_warned:
            logger.debug("session_config falling back to empty dict - context path may have changed")
            _session_config_warned = True

        return {}

    # Patch all available Context classes
    for _, context_class in _CONTEXT_CLASSES:
        if getattr(context_class, "_smithery_session_config_patched", False):
            continue  # Already patched

        # Add the property to this Context class
        context_class.session_config = session_config
        context_class._smithery_session_config_patched = True


class SmitheryFastMCP:
    """Wrapper that adds session config and CORS to FastMCP using global app wrapping."""

    def __init__(self, fastmcp_instance: FastMCP, config_schema: type[BaseModel] | None = None):
        self._fastmcp = fastmcp_instance
        self._config_schema = config_schema

        # Ensure Context class is patched for ctx.session_config access
        ensure_context_patched()

    def __getattr__(self, name: str):
        """Forward attribute access to wrapped FastMCP instance."""
        if hasattr(self._fastmcp, name):
            attr = getattr(self._fastmcp, name)

            # Intercept app creation methods to apply global wrapping
            if name in ('http_app', 'streamable_http_app') and callable(attr):
                return self._wrap_app_method(attr)

            return attr

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _wrap_app_method(self, original_method):
        """Wrap app creation methods to apply global middleware wrapping."""
        @functools.wraps(original_method)
        def wrapped_method(*args, **kwargs):
            # Create the base app (whatever FastMCP returns)
            app = original_method(*args, **kwargs)

            # Global SessionConfig wrapping - most robust approach
            app = SessionConfigMiddleware(app, config_schema=self._config_schema)

            # Global CORS wrapping - guarantees CORS headers on ALL responses (including errors)
            # Order: session-config → CORS, so CORS headers are present on schema/errors
            app = CORSMiddleware(
                app=app,
                allow_origins=["*"],
                allow_credentials=False,  # As per CORS analysis
                allow_methods=["GET", "POST"],
                allow_headers=["Content-Type", "Accept", "Authorization", "mcp-session-id", "mcp-protocol-version"],
                expose_headers=["mcp-session-id", "mcp-protocol-version"],
                max_age=86400,
            )

            return app

        return wrapped_method





def from_fastmcp(
    fastmcp_instance: FastMCP,
    *,
    config_schema: type[BaseModel] | None = None
) -> SmitheryFastMCP:
    """Add session config support and CORS to FastMCP. Config accessed via ctx.session_config."""
    return SmitheryFastMCP(fastmcp_instance, config_schema)




