"""HTTP response utilities for Smithery."""


from pydantic import ValidationError
from starlette.responses import JSONResponse


def create_error_response(
    status: int,
    title: str,
    detail: str,
    validation_error: ValidationError | None = None
) -> JSONResponse:
    """
    Create standardized error response.

    Args:
        status: HTTP status code
        title: Error title
        detail: Error detail message
        validation_error: Optional Pydantic validation error for detailed error info

    Returns:
        JSONResponse with standardized error format
    """
    content = {"title": title, "status": status, "detail": detail}

    if validation_error:
        content["errors"] = [
            {"param": ".".join(str(p) for p in err["loc"]), "reason": err["msg"]}
            for err in validation_error.errors()
        ]

    return JSONResponse(content=content, status_code=status)
