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
import time

# Utility functions
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} executed in {duration} seconds.")
        return result
    return wrapper


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
def filter_and_transform_df(
    context: AssetExecutionContext,
    json_items: List, 
    ) -> pd.DataFrame:
    """Filter and transform a list of JSON items into a list of records."""
    
    logger = get_dagster_logger()

    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_items if "forms" in item]

    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    df['flattened_forms'] = df.forms.apply(lambda x: [item['form'] for item in x])

    df['glosses'] = df.senses.apply(get_glosses_from_string)

    # if sandbox_transformed:
    #     sandboxing_transformation(df, preview_column=preview_column)

    filter_and_transform_df = df[['word', 'pos', 'glosses', 'forms', 'flattened_forms', 'lang']]

    context.add_output_metadata(
        metadata={
            "num_records": len(filter_and_transform_df),  # Metadata can be any key-value pair
            "preview": MetadataValue.md(filter_and_transform_df.head().to_markdown()),
            # The `MetadataValue` class has useful static methods to build Metadata
        }
    )

    logger.info(filter_and_transform_df.head())

    return filter_and_transform_df

@asset
def dataframe_to_records(
    filter_and_transform_df: pd.DataFrame
    ) -> List:
    """Convert DataFrame to a list of records, converting the "forms" column to JSON."""
    logger = get_dagster_logger()
    records = filter_and_transform_df.reset_index().to_records(index=False)

    # This will include the index name as the first column
    columns = ['index'] + list(filter_and_transform_df.columns)
    dataframe_to_records = [
        tuple(
            json.dumps(record[col], ensure_ascii=False) if col == "forms" else record[col]
            for col in columns
        )
        for record in records
    ]
    logger.info(dataframe_to_records)
    return dataframe_to_records