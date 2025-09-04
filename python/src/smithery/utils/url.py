import base64
import json
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def encode_config_to_base64(config: dict[str, Any]) -> str:
    """Encode config dict to base64 JSON string."""
    config_json = json.dumps(config)
    return base64.b64encode(config_json.encode("utf-8")).decode("utf-8")


def decode_config_from_base64(config_b64: str) -> dict[str, Any]:
    """Decode base64 JSON string to config dict. Raises ValueError on failure."""
    try:
        config_json = base64.b64decode(config_b64).decode("utf-8")
        return json.loads(config_json)
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"Failed to decode config parameter: {e}") from e


def create_smithery_url(base_url, config=None, api_key=None):
    """Create Smithery URL with optional base64 config and API key parameters."""
    # Parse the URL
    parsed_url = urlparse(base_url)

    # Parse existing query parameters
    query_params = parse_qs(parsed_url.query)

    # Add config if provided
    if config is not None:
        config_base64 = encode_config_to_base64(config)
        query_params["config"] = [config_base64]

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
