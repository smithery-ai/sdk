"""
Version Utilities for Testing

Utilities for version detection and conditional testing across different
FastMCP and MCP SDK versions.
"""
import importlib.util
import sys

import pytest  # type: ignore
from packaging import version

# Check if MCP SDK FastMCP is available
if importlib.util.find_spec("mcp.server.fastmcp"):
    import mcp  # type: ignore
    FASTMCP_AVAILABLE = True
    MCP_AVAILABLE = True
else:
    FASTMCP_AVAILABLE = False
    MCP_AVAILABLE = False
    mcp = None

# Try to import standalone fastmcp as well
try:
    import fastmcp  # type: ignore
    STANDALONE_FASTMCP_AVAILABLE = True
except ImportError:
    STANDALONE_FASTMCP_AVAILABLE = False
    fastmcp = None


def get_fastmcp_version() -> str | None:
    """Get FastMCP version string."""
    # Try standalone fastmcp first
    if STANDALONE_FASTMCP_AVAILABLE and fastmcp:
        version_attrs = ['__version__', 'version', 'VERSION']
        for attr in version_attrs:
            if hasattr(fastmcp, attr):
                return getattr(fastmcp, attr)

    # Try getting version from package metadata
    try:
        from importlib.metadata import version as get_version
        return get_version('fastmcp')
    except Exception:
        pass

    # Fallback: try mcp module (which contains FastMCP)
    if MCP_AVAILABLE and mcp:
        version_attrs = ['__version__', 'version', 'VERSION']
        for attr in version_attrs:
            if hasattr(mcp, attr):
                return getattr(mcp, attr)

        # Try submodules
        try:
            import mcp.server # type: ignore
            if hasattr(mcp.server, '__version__'):
                return mcp.server.__version__
        except (ImportError, AttributeError):
            pass

        try:
            import mcp.server.fastmcp # type: ignore
            if hasattr(mcp.server.fastmcp, '__version__'):
                return mcp.server.fastmcp.__version__
        except (ImportError, AttributeError):
            pass

    return None


def get_mcp_version() -> str | None:
    """Get MCP SDK version string."""
    # Try getting version from module attributes first
    if MCP_AVAILABLE and mcp:
        version_attrs = ['__version__', 'version', 'VERSION']
        for attr in version_attrs:
            if hasattr(mcp, attr):
                return getattr(mcp, attr)

    # Try getting version from package metadata
    try:
        from importlib.metadata import version as get_version
        return get_version('mcp')
    except Exception:
        pass

    return None


def parse_version(version_str: str | None) -> version.Version | None:
    """Parse version string into Version object."""
    if not version_str:
        return None

    try:
        return version.parse(version_str)
    except version.InvalidVersion:
        return None


def get_python_version() -> tuple[int, int, int]:
    """Get current Python version tuple."""
    return sys.version_info[:3]


class VersionRequirement:
    """Version requirement checker."""

    def __init__(self, package: str, min_version: str = None, max_version: str = None):
        self.package = package
        self.min_version = parse_version(min_version) if min_version else None
        self.max_version = parse_version(max_version) if max_version else None

        if package == 'fastmcp':
            self.current_version = parse_version(get_fastmcp_version())
        elif package == 'mcp':
            self.current_version = parse_version(get_mcp_version())
        else:
            raise ValueError(f"Unknown package: {package}")

    def is_satisfied(self) -> bool:
        """Check if version requirement is satisfied."""
        if not self.current_version:
            return False

        if self.min_version and self.current_version < self.min_version:
            return False

        if self.max_version and self.current_version > self.max_version:
            return False

        return True

    def skip_reason(self) -> str:
        """Get skip reason if requirement not satisfied."""
        if not self.current_version:
            return f"{self.package} not available"

        parts = []
        if self.min_version:
            parts.append(f">= {self.min_version}")
        if self.max_version:
            parts.append(f"<= {self.max_version}")

        req_str = " and ".join(parts) if parts else "any version"
        return f"{self.package} {self.current_version} does not satisfy requirement: {req_str}"


# Decorators for version-conditional testing
def requires_fastmcp(min_version: str = None, max_version: str = None):
    """Skip test if FastMCP version requirements not met."""
    req = VersionRequirement('fastmcp', min_version, max_version)
    return pytest.mark.skipif(not req.is_satisfied(), reason=req.skip_reason())


def requires_mcp(min_version: str = None, max_version: str = None):
    """Skip test if MCP SDK version requirements not met."""
    req = VersionRequirement('mcp', min_version, max_version)
    return pytest.mark.skipif(not req.is_satisfied(), reason=req.skip_reason())


def requires_python(min_version: str):
    """Skip test if Python version is too old."""
    min_ver = tuple(map(int, min_version.split('.')))
    current_ver = get_python_version()
    return pytest.mark.skipif(
        current_ver < min_ver,
        reason=f"Python {current_ver} < {min_ver}"
    )


# Feature detection utilities
def has_fastmcp_feature(feature: str) -> bool:
    """Check if FastMCP has a specific feature."""
    if not FASTMCP_AVAILABLE:
        return False

    feature_checks = {
        'tool_decorator': lambda: hasattr(fastmcp.FastMCP, 'tool'),
        'resource_decorator': lambda: hasattr(fastmcp.FastMCP, 'resource'),
        'prompt_decorator': lambda: hasattr(fastmcp.FastMCP, 'prompt'),
        'http_app': lambda: hasattr(fastmcp.FastMCP, 'http_app'),
        'streamable_http_app': lambda: hasattr(fastmcp.FastMCP, 'streamable_http_app'),
        'context_manager': lambda: hasattr(fastmcp.FastMCP, '__enter__'),
    }

    check_func = feature_checks.get(feature)
    if not check_func:
        return False

    try:
        return check_func()
    except Exception:
        return False


def requires_fastmcp_feature(feature: str):
    """Skip test if FastMCP doesn't have required feature."""
    return pytest.mark.skipif(
        not has_fastmcp_feature(feature),
        reason=f"FastMCP feature '{feature}' not available"
    )


# Version compatibility matrix
KNOWN_COMPATIBLE_VERSIONS = {
    # (fastmcp_version, mcp_version): compatibility_notes
    ("0.10.0", "0.9.0"): "Basic compatibility",
    ("0.11.0", "0.9.0"): "Enhanced features",
    ("0.12.0", "1.0.0"): "Latest stable",
}


def get_compatibility_notes() -> str:
    """Get compatibility notes for current version combination."""
    fastmcp_ver = get_fastmcp_version()
    mcp_ver = get_mcp_version()

    if not fastmcp_ver or not mcp_ver:
        return "Version information not available"

    key = (fastmcp_ver, mcp_ver)
    return KNOWN_COMPATIBLE_VERSIONS.get(key, "Unknown compatibility - testing recommended")


# Test reporting utilities
def report_test_environment():
    """Report current test environment versions."""
    fastmcp_ver = get_fastmcp_version() or "Not available"
    mcp_ver = get_mcp_version() or "Not available"
    python_ver = ".".join(map(str, get_python_version()))

    print("\n=== Test Environment ===")
    print(f"Python: {python_ver}")
    print(f"FastMCP: {fastmcp_ver}")
    print(f"MCP SDK: {mcp_ver}")
    print(f"Compatibility: {get_compatibility_notes()}")
    print("=" * 25)


if __name__ == "__main__":
    # Run this to see current environment
    report_test_environment()
