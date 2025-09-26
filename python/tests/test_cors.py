"""
Tests for CORS Functionality

Comprehensive tests for Cross-Origin Resource Sharing behavior across all endpoints.
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


class TestCORS:
    """Comprehensive CORS tests."""

    def test_cors_well_known_endpoint_no_origin(self):
        """Test well-known endpoint without Origin header - CORS headers only when needed."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.get("/.well-known/mcp-config")

            assert response.status_code == 200
            # CORSMiddleware only adds headers when Origin header is present or for preflight
            # This is the correct behavior - no CORS headers for regular requests without Origin
            cors_header_present = "access-control-allow-origin" in response.headers
            assert cors_header_present is False or response.headers["access-control-allow-origin"] == "*"

    def test_cors_well_known_endpoint_with_origin(self):
        """Test well-known endpoint with Origin header - CORS headers present."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.get(
                "/.well-known/mcp-config",
                headers={"Origin": "https://example.com"}
            )

            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == "*"
            # Verify other CORS headers are present
            assert "access-control-expose-headers" in response.headers

    def test_cors_preflight_well_known_endpoint(self):
        """Test preflight request for well-known endpoint."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.options(
                "/.well-known/mcp-config",
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )

            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == "*"
            assert "GET" in response.headers["access-control-allow-methods"]
            assert "Content-Type" in response.headers["access-control-allow-headers"]

    def test_cors_mcp_endpoint_no_origin(self):
        """Test MCP endpoint without Origin header - CORS behavior depends on response type."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.post(
                "/mcp",
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            # For error responses, CORS headers might be present even without Origin
            # This is because the middleware may add them for all HTTP responses
            if "access-control-allow-origin" in response.headers:
                assert response.headers["access-control-allow-origin"] == "*"

    def test_cors_mcp_endpoint_with_origin(self):
        """Test MCP endpoint with Origin header - CORS headers present."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.post(
                "/mcp",
                headers={"Origin": "https://example.com"},
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            assert response.headers["access-control-allow-origin"] == "*"

    def test_cors_preflight_mcp_endpoint(self):
        """Test preflight request for MCP endpoint."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.options(
                "/mcp",
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type, mcp-session-id"
                }
            )

            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == "*"
            assert "POST" in response.headers["access-control-allow-methods"]
            assert "Content-Type" in response.headers["access-control-allow-headers"]
            assert "mcp-session-id" in response.headers["access-control-allow-headers"]

    def test_cors_error_responses(self):
        """Test that error responses include CORS headers when Origin is present."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test 404 error with CORS
            response = client.get(
                "/non-existent-endpoint",
                headers={"Origin": "https://example.com"}
            )

            assert response.status_code == 404
            assert response.headers["access-control-allow-origin"] == "*"

            # Test reserved parameter error with CORS
            response = client.post(
                "/mcp?api_key=test123",
                headers={"Origin": "https://example.com"},
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            assert response.status_code == 400
            assert response.headers["access-control-allow-origin"] == "*"

    def test_cors_config_validation_error(self):
        """Test that config validation errors include CORS headers."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            # Test validation error with CORS
            response = client.post(
                "/mcp?timeout=invalid",
                headers={"Origin": "https://example.com"},
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {}
                }
            )

            assert response.status_code == 422
            assert response.headers["access-control-allow-origin"] == "*"

    def test_cors_headers_configuration(self):
        """Test that CORS headers are configured correctly."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.options(
                "/mcp",
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type, Accept, Authorization, mcp-session-id, mcp-protocol-version"
                }
            )

            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == "*"

            # Check that all expected methods are allowed
            allowed_methods = response.headers["access-control-allow-methods"]
            assert "GET" in allowed_methods
            assert "POST" in allowed_methods

            # Check that all expected headers are allowed
            allowed_headers = response.headers["access-control-allow-headers"]
            assert "Content-Type" in allowed_headers
            assert "Accept" in allowed_headers
            assert "Authorization" in allowed_headers
            assert "mcp-session-id" in allowed_headers
            assert "mcp-protocol-version" in allowed_headers

            # Check exposed headers (may not be in OPTIONS response)
            if "access-control-expose-headers" in response.headers:
                exposed_headers = response.headers["access-control-expose-headers"]
                assert "mcp-session-id" in exposed_headers
                assert "mcp-protocol-version" in exposed_headers

    def test_cors_credentials_disabled(self):
        """Test that credentials are disabled (allow-credentials=False)."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.options(
                "/mcp",
                headers={
                    "Origin": "https://specific-origin.com",
                    "Access-Control-Request-Method": "POST"
                }
            )

            assert response.status_code == 200
            # With allow_credentials=False, origin should be * not reflected
            assert response.headers["access-control-allow-origin"] == "*"
            # Should not have allow-credentials header or it should be false
            credentials_header = response.headers.get("access-control-allow-credentials")
            assert credentials_header is None or credentials_header.lower() == "false"

    def test_cors_max_age(self):
        """Test that preflight cache max-age is set correctly."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        with TestClient(app) as client:
            response = client.options(
                "/mcp",
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "POST"
                }
            )

            assert response.status_code == 200
            # Check that max-age is set (86400 = 24 hours)
            max_age = response.headers.get("access-control-max-age")
            assert max_age == "86400"

    def test_cors_multiple_origins(self):
        """Test CORS behavior with different origins."""
        fastmcp_server = FastMCP(name="test-server")
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)
        app = smithery_server.streamable_http_app()

        origins = [
            "https://example.com",
            "https://another-domain.org",
            "http://localhost:3000",
            "https://app.smithery.ai"
        ]

        with TestClient(app) as client:
            for origin in origins:
                response = client.get(
                    "/.well-known/mcp-config",
                    headers={"Origin": origin}
                )

                assert response.status_code == 200
                # All origins should get * due to allow_origins=["*"]
                assert response.headers["access-control-allow-origin"] == "*"


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_cors.py -v
    pytest.main([__file__, "-v"])
