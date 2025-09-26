"""
Tests for Smithery FastMCP Integration

Tests the integration, CORS, and wrapper functionality.
"""
import pytest
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from starlette.testclient import TestClient

from smithery.server.fastmcp_patch import from_fastmcp

from .utils.version_utils import requires_fastmcp_feature


class ConfigSchema(BaseModel):
    """Configuration schema for testing."""

    api_key: str = Field(description="API key for authentication")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


class TestSmitheryIntegration:
    """Test the SmitheryFastMCP wrapper integration."""


    def test_backward_compatibility_streamable_http_app(self):
        """Test that streamable_http_app() still works (backward compatibility)."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)

        # Should be able to call the deprecated method
        app = smithery_server.streamable_http_app()

        # Should still work and have CORS/config middleware
        with TestClient(app) as client:
            response = client.get("/.well-known/mcp-config")
            assert response.status_code == 200

    def test_method_forwarding(self):
        """Test that non-intercepted methods are forwarded to FastMCP."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server)

        # Should forward attribute access
        assert smithery_server.name == "test-server"

        # Should forward method calls
        assert callable(smithery_server.run)



class TestIntegrationWithFastMCP:
    """Integration tests with actual FastMCP functionality."""

    @requires_fastmcp_feature('tool_decorator')
    def test_with_fastmcp_tool(self):
        """Test that tools work correctly with Smithery wrapper."""
        fastmcp_server = FastMCP(name="test-server")

        # Add a simple tool
        @fastmcp_server.tool()
        def hello_tool(name: str) -> str:
            """Say hello to someone."""
            return f"Hello, {name}!"

        # Wrap with Smithery
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Should be able to get schema
            response = client.get("/.well-known/mcp-config")
            assert response.status_code == 200

            # And tools should still work through the MCP protocol
            # (Full MCP testing would require more setup)


class TestImportCompatibility:
    """Test that all required imports work across versions."""

    def test_required_imports(self):
        """Test that all required imports work."""
        imports_to_test = [
            "mcp.server.fastmcp.FastMCP",
            "mcp.server.fastmcp.Context",
            "pydantic.BaseModel",
            "starlette.testclient.TestClient",
            "starlette.middleware.cors.CORSMiddleware",
        ]

        failed_imports = []

        for import_path in imports_to_test:
            try:
                module_path, class_name = import_path.rsplit(".", 1)
                module = __import__(module_path, fromlist=[class_name])
                getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                failed_imports.append(f"{import_path}: {e}")

        if failed_imports:
            pytest.fail("Failed imports:\n" + "\n".join(failed_imports))


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_integration.py -v
    pytest.main([__file__, "-v"])
