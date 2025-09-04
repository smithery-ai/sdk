"""HTTP response utilities for Smithery."""


from typing import Any

from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse


def get_config_schema_dict(config_schema: type[BaseModel]) -> dict[str, Any]:
    """Convert Pydantic model to JSON schema dict for frontend consumption."""
    try:
        return config_schema.model_json_schema()
    except Exception:
        # Fallback to empty schema if conversion fails
        return {"type": "object", "properties": {}}


def create_error_response(
    status: int,
    title: str,
    detail: str,
    validation_error: ValidationError | None = None,
    config_schema: dict | None = None,
    instance: str | None = None
) -> JSONResponse:
    """Create standardized error response. Includes validation details if provided.

    For 422 responses, includes configSchema in data field for frontend consumption.
    """
    content = {"title": title, "status": status, "detail": detail}

    if instance:
        content["instance"] = instance

    if validation_error:
        content["errors"] = [
            {"param": ".".join(str(p) for p in err["loc"]), "reason": err["msg"]}
            for err in validation_error.errors()
        ]

    # For 422 responses, include config schema at root level (matches TypeScript SDK)
    if status == 422 and config_schema:
        content["configSchema"] = config_schema

    # Add CORS headers for browser compatibility
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Accept, mcp-session-id, mcp-protocol-version",
        "Access-Control-Expose-Headers": "mcp-session-id, mcp-protocol-version",
    }

    return JSONResponse(content=content, status_code=status, headers=headers)
