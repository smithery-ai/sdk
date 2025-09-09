import json
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def append_config_as_dot_params(
    query_params: dict[str, list[str]], config: Any
) -> None:
    """Flatten config into dot-notation query parameters on query_params.

    Arrays are indexed using numeric segments (e.g., arr.0=value).
    Non-string primitives are JSON-encoded (true/false/null/numbers),
    while strings are used as-is.
    """

    def add(path_parts: list[str], value: Any) -> None:
        if isinstance(value, list):
            for index, item in enumerate(value):
                add([*path_parts, str(index)], item)
            return
        if isinstance(value, dict):
            for key, nested in value.items():
                add([*path_parts, str(key)], nested)
            return

        key = ".".join(path_parts)
        if isinstance(value, str):
            string_value = value
        else:
            # Use JSON to preserve booleans (true/false), null, and numbers
            string_value = json.dumps(value)
        query_params.setdefault(key, []).append(string_value)

    if isinstance(config, dict):
        for key, value in config.items():
            add([str(key)], value)


def create_smithery_url(base_url: str, config: dict[str, Any] | None = None, api_key: str | None = None) -> str:
    """Create Smithery URL with config encoded using dot-notation parameters.

    Example: https://host/namespace/mcp?model.name=gpt-4&debug=true
    """
    parsed_url = urlparse(base_url)

    # Parse existing query parameters
    query_params = parse_qs(parsed_url.query)

    # Add config if provided (as dot-notation params)
    if config is not None:
        append_config_as_dot_params(query_params, config)

    # Add API key if provided
    if api_key:
        query_params["api_key"] = [api_key]

    # Rebuild the query string
    new_query = urlencode(query_params, doseq=True)

    # Rebuild the URL with the new query string
    url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment,
        )
    )
    return url
