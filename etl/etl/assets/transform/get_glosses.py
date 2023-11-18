import requests
import json
from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)
from typing import List, Tuple

import pandas as pd
import ast
import json

######
###### get glosses ######

def string_to_list(s):
    """Convert a JSON string or lists to a Python list."""
    return ast.literal_eval(str(s))

def extract_glosses(dicts_list):
    """Extract glosses from a list of dictionaries."""
    return [item.get('glosses', [""]) for item in dicts_list] 

def flatten_list_of_lists(list_of_lists):
    """Flatten a list of lists into a single list."""
    return [item for sublist in list_of_lists for item in sublist]

def get_glosses_from_string(s):
    """Extract and flatten glosses from a JSON string."""
    dicts_list = string_to_list(s)
    glosses_list_of_lists = extract_glosses(dicts_list)
    flattened_glosses = flatten_list_of_lists(glosses_list_of_lists)
    return ', '.join(flattened_glosses)

@asset 
def get_glosses_df(
    context: AssetExecutionContext,
    start_process_df: pd.DataFrame, 
) -> pd.Series:
    logger = get_dagster_logger()

    df = start_process_df

    get_glosses_df = df.senses.apply(get_glosses_from_string)

    return get_glosses_df