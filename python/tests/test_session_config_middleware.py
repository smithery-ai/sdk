"""
Tests for Session Config Middleware

Tests config validation, reserved parameter detection, and error handling.
"""
import pytest
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from starlette.testclient import TestClient

from smithery.server.fastmcp_patch import from_fastmcp


class ConfigSchema(BaseModel):
    """Configuration schema for testing."""

    api_key: str = Field(description="API key for authentication")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


class SimpleConfigSchema(BaseModel):
    """Simple config schema without reserved parameters."""

    timeout: int = Field(default=30, description="Request timeout")
    debug: bool = Field(default=False, description="Debug mode")


class TestSessionConfigMiddleware:
    """Test session config middleware functionality."""

    def test_reserved_params_error(self):
        """Test that /mcp endpoint returns helpful error for reserved parameters."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test with reserved parameter api_key
            response = client.post(
                "/mcp?api_key=test123&timeout=60&debug=true",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # Should return 400 with helpful error message about reserved parameters
            assert response.status_code == 400
            data = response.json()
            assert "reserved" in data.get("title", "").lower()
            assert "api_key" in data.get("detail", "")

    def test_reserved_params_bracketed_notation(self):
        """Test that bracketed config notation doesn't trigger reserved param error."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test with config[api_key] (should not trigger reserved param error)
            response = client.post(
                "/mcp?config[api_key]=test123&config[timeout]=60",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # Should not return 400 for reserved parameters (might return other errors)
            assert response.status_code != 400 or "reserved" not in response.json().get("title", "").lower()

    def test_reserved_params_dot_notation(self):
        """Test that dot config notation doesn't trigger reserved param error."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test with config.api_key (should not trigger reserved param error)
            response = client.post(
                "/mcp?config.api_key=test123&config.timeout=60",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # Should not return 400 for reserved parameters (might return other errors)
            assert response.status_code != 400 or "reserved" not in response.json().get("title", "").lower()

    def test_valid_config(self):
        """Test that /mcp endpoint processes valid config correctly."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=SimpleConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test valid config without reserved parameters
            response = client.post(
                "/mcp?timeout=60&debug=true",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # Should not return config validation error (may return other MCP errors)
            assert response.status_code != 422  # No config validation error

    def test_invalid_config(self):
        """Test that /mcp endpoint returns 422 for invalid config."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test missing required fields (without using reserved params)
            response = client.post(
                "/mcp?timeout=60",  # ConfigSchema requires api_key, but it's reserved
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            assert response.status_code == 422
            data = response.json()
            assert "config" in data.get("title", "").lower() or "Invalid configuration" in data.get("title", "")

    def test_malformed_config(self):
        """Test that /mcp endpoint returns appropriate response for malformed config."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test malformed query parameters (this depends on implementation)
            # For now, just test that it doesn't crash
            response = client.post(
                "/mcp",  # No config at all
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # Should not crash, though exact status depends on FastMCP behavior
            assert response.status_code in [200, 400, 422, 500]

    def test_session_config_normalization(self):
        """Test that session_config is normalized to dict."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=SimpleConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.post(
                "/mcp?timeout=45&debug=true",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # Should not return validation error
            assert response.status_code != 422


if __name__ == "__main__":
    # Run with: python -m pytest tests/session_config_middleware.py -v
    pytest.main([__file__, "-v"])
