import requests
import json
from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger
)

from typing import Dict, List

@asset
def json_all_words() -> List:
    """
    Fetches the content from the given URL and parses it as JSON.

    Args:
    - url (str): The URL to fetch the data from.

    Returns:
    - list[dict]: A list of dictionaries parsed from the JSON content.
    """
    
    url = "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"

    ## "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-verb/kaikki_dot_org-dictionary-Polish-by-pos-verb.json"

    ## "https://kaikki.org/dictionary/Polish/by-pos-adj/kaikki_dot_org-dictionary-Polish-by-pos-adj.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-noun/kaikki_dot_org-dictionary-Polish-by-pos-noun.json"

    response = requests.get(url)
    # Raise an exception if the response contains an HTTP error status code.
    response.raise_for_status()
    # Get the raw text content
    raw_content = response.text
    # Split the content by newline to get individual JSON strings
    json_strs = [line for line in raw_content.split("\n") if line.strip()]
    # Convert each line to a Python object
    json_all_words = [json.loads(item) for item in json_strs]
    return json_all_words

@asset
def json_verbs() -> List:
    """
    Fetches the content from the given URL and parses it as JSON.

    Args:
    - url (str): The URL to fetch the data from.

    Returns:
    - list[dict]: A list of dictionaries parsed from the JSON content.
    """
    
    url = "https://kaikki.org/dictionary/Polish/by-pos-verb/kaikki_dot_org-dictionary-Polish-by-pos-verb.json"

    ## "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-verb/kaikki_dot_org-dictionary-Polish-by-pos-verb.json"

    ## "https://kaikki.org/dictionary/Polish/by-pos-adj/kaikki_dot_org-dictionary-Polish-by-pos-adj.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-noun/kaikki_dot_org-dictionary-Polish-by-pos-noun.json"

    response = requests.get(url)
    # Raise an exception if the response contains an HTTP error status code.
    response.raise_for_status()
    # Get the raw text content
    raw_content = response.text
    # Split the content by newline to get individual JSON strings
    json_strs = [line for line in raw_content.split("\n") if line.strip()]
    # Convert each line to a Python object
    json_verbs = [json.loads(item) for item in json_strs]
    return json_verbs

@asset
def json_adjectives() -> List:
    """
    Fetches the content from the given URL and parses it as JSON.

    Args:
    - url (str): The URL to fetch the data from.

    Returns:
    - list[dict]: A list of dictionaries parsed from the JSON content.
    """
    
    url = "https://kaikki.org/dictionary/Polish/by-pos-adj/kaikki_dot_org-dictionary-Polish-by-pos-adj.json"

    ## "https://kaikki.org/dictionary/Polish/kaikki.org-dictionary-Polish.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-verb/kaikki_dot_org-dictionary-Polish-by-pos-verb.json"

    ## "https://kaikki.org/dictionary/Polish/by-pos-adj/kaikki_dot_org-dictionary-Polish-by-pos-adj.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-det/kaikki_dot_org-dictionary-Polish-by-pos-det.json"
    ## "https://kaikki.org/dictionary/Polish/by-pos-noun/kaikki_dot_org-dictionary-Polish-by-pos-noun.json"

    response = requests.get(url)
    # Raise an exception if the response contains an HTTP error status code.
    response.raise_for_status()
    # Get the raw text content
    raw_content = response.text
    # Split the content by newline to get individual JSON strings
    json_strs = [line for line in raw_content.split("\n") if line.strip()]
    # Convert each line to a Python object
    json_adjectives = [json.loads(item) for item in json_strs]
    return json_adjectives

@asset
def json_adverbs() -> List:
    """
    Fetches the content from the given URL and parses it as JSON.

    Args:
    - url (str): The URL to fetch the data from.

    Returns:
    - list[dict]: A list of dictionaries parsed from the JSON content.
    """
    
    url = "https://kaikki.org/dictionary/Polish/by-pos-adv/kaikki_dot_org-dictionary-Polish-by-pos-adv.json"

    response = requests.get(url)
    # Raise an exception if the response contains an HTTP error status code.
    response.raise_for_status()
    # Get the raw text content
    raw_content = response.text
    # Split the content by newline to get individual JSON strings
    json_strs = [line for line in raw_content.split("\n") if line.strip()]
    # Convert each line to a Python object
    json_adverbs = [json.loads(item) for item in json_strs]
    return json_adverbs