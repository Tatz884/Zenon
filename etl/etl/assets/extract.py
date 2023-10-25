import requests
import json
from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger
)

from typing import Dict, List

@asset
def json_items() -> List:
    """
    Fetches the content from the given URL and parses it as JSON.

    Args:
    - url (str): The URL to fetch the data from.

    Returns:
    - list[dict]: A list of dictionaries parsed from the JSON content.
    """
    
    url = "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"

    response = requests.get(url)
    # Raise an exception if the response contains an HTTP error status code.
    response.raise_for_status()
    # Get the raw text content
    raw_content = response.text
    # Split the content by newline to get individual JSON strings
    json_strs = [line for line in raw_content.split("\n") if line.strip()]
    # Convert each line to a Python object
    json_items = [json.loads(item) for item in json_strs]
    logger = get_dagster_logger()
    logger.info("type")
    logger.info(json_items[0])
    logger.info(type(json_items[0]))
    return json_items