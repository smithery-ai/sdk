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
    config_schema: dict | None = None
) -> JSONResponse:
    """Create standardized error response. Includes validation details if provided.
    
    For 422 responses, includes configSchema in data field for frontend consumption.
    """
    content = {"title": title, "status": status, "detail": detail}

    if validation_error:
        content["errors"] = [
            {"param": ".".join(str(p) for p in err["loc"]), "reason": err["msg"]}
            for err in validation_error.errors()
        ]

    # For 422 responses, include config schema in data field for frontend
    if status == 422 and config_schema:
        content["data"] = {"configSchema": config_schema}

    return JSONResponse(content=content, status_code=status)
