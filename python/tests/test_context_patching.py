"""
Tests for Context Patching

Tests the session_config property on FastMCP Context and idempotent patching.
"""
import pytest
from pydantic import BaseModel, Field
from starlette.testclient import TestClient

from smithery.server.fastmcp_patch import from_fastmcp


# Parameterized imports for both MCP SDK and standalone FastMCP
def get_fastmcp_imports():
    """Get available FastMCP import configurations."""
    imports = []

    # Try MCP SDK version
    try:
        from mcp.server.fastmcp import Context, FastMCP
        imports.append(("mcp_sdk", Context, FastMCP))
    except ImportError:
        pass

    # Try standalone FastMCP version
    try:
        from fastmcp import Context, FastMCP
        imports.append(("standalone", Context, FastMCP))
    except ImportError:
        pass

    return imports

# Get available import configurations
FASTMCP_IMPORTS = get_fastmcp_imports()


class ConfigSchema(BaseModel):
    """Configuration schema for testing."""

    api_key: str = Field(description="API key for authentication")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


@pytest.mark.skipif(not FASTMCP_IMPORTS, reason="No FastMCP package available")
class TestContextPatching:
    """Test Context patching functionality."""

    @pytest.mark.parametrize("import_source,Context,FastMCP", FASTMCP_IMPORTS)
    def test_context_patching(self, import_source, Context, FastMCP):
        """Test that Context.session_config is available."""
        # Test that the Context class has been patched
        fastmcp_server = FastMCP(name=f"test-server-{import_source}")
        from_fastmcp(fastmcp_server, config_schema=ConfigSchema)

        # Should have patched the Context class
        assert hasattr(Context, 'session_config')

        # The property should be a property descriptor
        assert isinstance(Context.session_config, property)

        # Test idempotent patching
        assert hasattr(Context, '_smithery_session_config_patched')
        assert Context._smithery_session_config_patched is True

        # Test that it handles the no-context case gracefully
        # (We can't easily test the actual context access without a full MCP request setup)

    @pytest.mark.parametrize("import_source,Context,FastMCP", FASTMCP_IMPORTS)
    def test_idempotent_context_patching(self, import_source, Context, FastMCP):
        """Test that context patching is idempotent across multiple instances."""
        fastmcp_server1 = FastMCP(name=f"test-server-1-{import_source}")
        fastmcp_server2 = FastMCP(name=f"test-server-2-{import_source}")

        smithery_server1 = from_fastmcp(fastmcp_server1)
        smithery_server2 = from_fastmcp(fastmcp_server2)

        # Both should reference the same patched Context class
        assert hasattr(Context, 'session_config')
        assert hasattr(Context, '_smithery_session_config_patched')
        assert Context._smithery_session_config_patched is True

        # Should work for both servers
        app1 = smithery_server1.streamable_http_app()
        app2 = smithery_server2.streamable_http_app()

        with TestClient(app1) as client1:
            response1 = client1.get("/.well-known/mcp-config")
            assert response1.status_code == 200

        with TestClient(app2) as client2:
            response2 = client2.get("/.well-known/mcp-config")
            assert response2.status_code == 200

    @pytest.mark.parametrize("import_source,Context,FastMCP", FASTMCP_IMPORTS)
    def test_multiple_wrapper_instances(self, import_source, Context, FastMCP):
        """Test that multiple wrapper instances don't interfere with each other."""
        # Create separate FastMCP instances (session managers can't be reused)
        fastmcp_server1 = FastMCP(name=f"test-server-1-{import_source}")
        fastmcp_server2 = FastMCP(name=f"test-server-2-{import_source}")

        smithery_server1 = from_fastmcp(fastmcp_server1, config_schema=ConfigSchema)
        smithery_server2 = from_fastmcp(fastmcp_server2, config_schema=ConfigSchema)

        # Should be able to create apps from different servers
        app1 = smithery_server1.streamable_http_app()
        app2 = smithery_server2.streamable_http_app()

        # Both should work independently
        with TestClient(app1) as client1:
            response1 = client1.get("/.well-known/mcp-config")
            assert response1.status_code == 200

        with TestClient(app2) as client2:
            response2 = client2.get("/.well-known/mcp-config")
            assert response2.status_code == 200


if __name__ == "__main__":
    # Run with: python -m pytest tests/context_patching.py -v
    pytest.main([__file__, "-v"])
