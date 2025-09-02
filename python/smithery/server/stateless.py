"""
Stateless MCP Server implementation for Python.

This module provides a stateless server that creates a new server instance for each request.
No session state is maintained, making it ideal for stateless API integrations and serverless environments.
"""

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http import StreamableHTTPServerTransport
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


class StatelessServerOptions(BaseModel):
    """Configuration options for the stateless server."""
    config_schema: Optional[type[BaseModel]] = None
    
    class Config:
        arbitrary_types_allowed = True


def parse_and_validate_config(
    request: Request,
    config_schema: Optional[type[BaseModel]] = None
) -> BaseModel:
    """Parse and validate config from request with optional Pydantic schema validation."""
    config = {}
    
    # 1. Process base64-encoded config parameter if present
    from .stateful import parse_express_request_config, parse_dot_notation_config
    
    try:
        base_config = parse_express_request_config(request)
        config.update(base_config)
    except ValueError as e:
        raise ValueError(f"Invalid config parameter: {e}")
    
    # 2. Process dot-notation config parameters
    query_dict = dict(request.query_params)
    dot_config = parse_dot_notation_config(query_dict)
    config.update(dot_config)
    
    # 3. Validate against schema if provided
    if config_schema:
        try:
            return config_schema(**config)
        except Exception as e:
            raise ValueError(f"Config validation failed: {e}")
    
    # Return empty config instance if no schema provided
    return BaseModel()


def create_stateless_server(
    mcp_server: FastMCP,
    options: Optional[StatelessServerOptions] = None
) -> Starlette:
    """
    Create a stateless server for handling MCP requests.
    
    Each request creates a new server instance - no session state is maintained.
    This is ideal for stateless API integrations and serverless environments.
    
    Args:
        mcp_server: FastMCP server instance to use as template for handling requests
        options: Configuration options including optional schema validation
        
    Returns:
        Starlette application
    """
    if options is None:
        options = StatelessServerOptions()
    
    async def mcp_post_handler(request: Request) -> Response:
        """Handle POST requests for client-to-server communication."""
        # In stateless mode, create a new instance of transport and server for each request
        # to ensure complete isolation. A single instance would cause request ID collisions
        # when multiple clients connect concurrently.
        
        try:
            # Validate config for all requests in stateless mode
            try:
                parse_and_validate_config(request, options.config_schema)
            except ValueError as e:
                return JSONResponse(
                    status_code=400,
                    content={
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32602,
                            "message": str(e)
                        },
                        "id": None
                    }
                )
            
            # Create a new transport for this request (no session management)
            transport = StreamableHTTPServerTransport(
                session_id_generator=None
            )
            
            # Connect the MCP server to the transport
            await mcp_server.connect(transport)
            
            # Handle the request directly
            # Read the request body
            body = await request.json()
            
            # Create a new request object with the body we already read
            from starlette.requests import Request as StarletteRequest
            
            # We need to recreate the request with the body since we already consumed it
            body_bytes = json.dumps(body).encode()
            
            # Create a new scope with the body
            scope = request.scope.copy()
            
            # Create a simple receive callable that returns the body
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            
            # Create new request with the body
            new_request = StarletteRequest(scope, receive)
            
            return await transport.handle_request(new_request)
            
        except Exception as error:
            print(f"Error handling MCP request: {error}")
            return JSONResponse(
                status_code=500,
                content={
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": "Internal server error"
                    },
                    "id": None
                }
            )
    
    async def mcp_get_handler(request: Request) -> Response:
        """SSE notifications not supported in stateless mode."""
        return JSONResponse(
            status_code=405,
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Method not allowed."
                },
                "id": None
            }
        )
    
    async def mcp_delete_handler(request: Request) -> Response:
        """Session termination not needed in stateless mode."""
        return JSONResponse(
            status_code=405,
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Method not allowed."
                },
                "id": None
            }
        )
    
    async def mcp_config_handler(request: Request) -> Response:
        """Handle GET requests for /.well-known/mcp-config endpoint."""
        base_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # If we have a Pydantic schema, convert it to JSON Schema
        if options.config_schema:
            try:
                # Create a dummy instance to get the schema
                schema_dict = options.config_schema.model_json_schema()
                base_schema = schema_dict
            except Exception:
                pass  # Fall back to empty schema
        
        config_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{request.url.scheme}://{request.headers.get('host', 'localhost')}/.well-known/mcp-config",
            "title": "MCP Session Configuration",
            "description": "Schema for the /mcp endpoint configuration",
            "x-mcp-version": "1.0",
            "x-query-style": "dot+bracket",
            **base_schema
        }
        
        return JSONResponse(
            content=config_schema,
            headers={"Content-Type": "application/schema+json; charset=utf-8"}
        )
    
    # Create Starlette application
    routes = [
        Route("/mcp", mcp_post_handler, methods=["POST"]),
        Route("/mcp", mcp_get_handler, methods=["GET"]),
        Route("/mcp", mcp_delete_handler, methods=["DELETE"]),
        Route("/.well-known/mcp-config", mcp_config_handler, methods=["GET"]),
    ]
    
    middleware = [
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    ]
    
    app = Starlette(routes=routes, middleware=middleware)
    
    return app
