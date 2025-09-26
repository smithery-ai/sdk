"""
Tests for Well-Known Configuration Endpoint

Tests the /.well-known/mcp-config endpoint functionality including schema generation and CORS.
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


class TestWellKnownEndpoint:
    """Test the /.well-known/mcp-config endpoint."""

    def test_endpoint_no_schema(self):
        """Test /.well-known/mcp-config endpoint without schema."""
        # Create FastMCP server
        fastmcp_server = FastMCP(name="test-server")

        # Wrap with Smithery (no schema)
        smithery_server = from_fastmcp(fastmcp_server)

        # Create ASGI app
        app = smithery_server.streamable_http_app()

        # Create test client
        with TestClient(app) as client:
            response = client.get("/.well-known/mcp-config")

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/schema+json; charset=utf-8"
            assert response.headers["cache-control"] == "no-cache, no-store, must-revalidate"

            data = response.json()
            assert data == {"message": "No configuration schema available"}

    def test_endpoint_with_schema(self):
        """Test /.well-known/mcp-config endpoint with schema."""
        # Create FastMCP server
        fastmcp_server = FastMCP(name="test-server")

        # Wrap with Smithery (with schema)
        smithery_server = from_fastmcp(fastmcp_server, config_schema=ConfigSchema)

        # Create ASGI app
        app = smithery_server.streamable_http_app()

        # Create test client
        with TestClient(app) as client:
            response = client.get("/.well-known/mcp-config")

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/schema+json; charset=utf-8"
            assert response.headers["cache-control"] == "no-cache, no-store, must-revalidate"

            data = response.json()

            # Should have JSON Schema structure
            assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
            assert "testserver" in data["$id"]  # Test client uses testserver
            assert data["title"] == "ConfigSchema"  # Title from Pydantic model
            assert data["description"] == "Configuration schema for testing."
            assert data["x-query-style"] == "dot+bracket"

            # Should have the ConfigSchema properties
            assert "properties" in data
            assert "api_key" in data["properties"]
            assert "timeout" in data["properties"]
            assert "debug" in data["properties"]

            # Check property details
            assert data["properties"]["api_key"]["type"] == "string"
            assert data["properties"]["timeout"]["type"] == "integer"
            assert data["properties"]["timeout"]["default"] == 30
            assert data["properties"]["debug"]["type"] == "boolean"
            assert data["properties"]["debug"]["default"] is False



if __name__ == "__main__":
    # Run with: python -m pytest tests/well_known_endpoint.py -v
    pytest.main([__file__, "-v"])
