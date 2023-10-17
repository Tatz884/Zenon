import requests
import json

def extract_json_data(url):
    response = requests.get(url)
    # Raise an exception if the response contains an HTTP error status code.
    response.raise_for_status()
    # Get the raw text content
    raw_content = response.text
    # Split the content by newline to get individual JSON strings
    json_strs = [line for line in raw_content.split("\n") if line.strip()]
    # Convert each line to a Python object
    json_items = [json.loads(item) for item in json_strs]
    return json_items
