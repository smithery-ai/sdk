import base64
import json
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def encode_config_to_base64(config: dict[str, Any]) -> str:
    """
    Encode a configuration dictionary to base64.

    Args:
        config: Configuration dictionary to encode

    Returns:
        Base64-encoded JSON string
    """
    config_json = json.dumps(config)
    return base64.b64encode(config_json.encode("utf-8")).decode("utf-8")


def decode_config_from_base64(config_b64: str) -> dict[str, Any]:
    """
    Decode a base64-encoded configuration string.

    Args:
        config_b64: Base64-encoded JSON string

    Returns:
        Configuration dictionary, or empty dict if decoding fails
    """
    try:
        config_json = base64.b64decode(config_b64).decode("utf-8")
        return json.loads(config_json)
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def create_smithery_url(base_url, config=None, api_key=None):
    """
    Create a Smithery URL with optional configuration parameters encoded in base64 and optional API key.

    Args:
        base_url (str): The base URL to use
        config (dict, optional): Configuration object to encode and add as a query parameter
        api_key (str, optional): API key to add as a query parameter

    Returns:
        str: The complete URL with any configuration parameters and API key added
    """
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
