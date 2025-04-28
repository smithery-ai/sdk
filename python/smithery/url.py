import json
import base64
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


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
        config_json = json.dumps(config)
        config_base64 = base64.b64encode(config_json.encode("utf-8")).decode("utf-8")
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
