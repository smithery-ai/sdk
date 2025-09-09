"""Configuration parsing utilities for Smithery."""

import json
from typing import Any
from urllib.parse import parse_qsl


def parse_config_from_query_string(query_string: str) -> dict[str, Any]:
    """Parse config from query string using dot notation (e.g., a.b=c&flag=true)."""
    if not query_string:
        return {}

    # Parse query parameters
    query_params = dict(parse_qsl(query_string))
    config: dict[str, Any] = {}

    # Process dot-notation config parameters (foo=bar, a.b=c)
    # This allows URL params like ?server.host=localhost&server.port=8080&debug=true
    for key, value in query_params.items():
        # Skip reserved parameters
        if key in ("api_key", "profile"):
            continue

        path_parts = key.split(".")

        # Try to parse value as JSON (for booleans, numbers, objects)
        parsed_value: Any = value
        try:
            parsed_value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            # If parsing fails, use the raw string value
            pass

        # Set nested path in config
        set_nested_value(config, path_parts, parsed_value)

    return config


def parse_config_from_asgi_scope(scope: dict[str, Any]) -> dict[str, Any]:
    """Parse config from ASGI scope query string."""
    # Extract query string from scope
    query_string = scope.get("query_string", b"").decode("utf-8")
    return parse_config_from_query_string(query_string)


def set_nested_value(obj: dict[str, Any], path_parts: list[str], value: Any) -> None:
    """Set nested dict value using path parts. E.g. ["server", "host"] sets obj["server"]["host"]."""
    current = obj
    for part in path_parts[:-1]:
        if part not in current:
            current[part] = {}
        elif not isinstance(current[part], dict):
            # If we encounter a non-dict value in the path, convert it to dict
            current[part] = {}
        current = current[part]

    # Set the final value
    current[path_parts[-1]] = value
