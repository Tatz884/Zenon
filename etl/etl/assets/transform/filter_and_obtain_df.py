from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)
from typing import List

import pandas as pd


def filter_tags(data):
    return [item for item in data if item.get('tags') not in [['table-tags'], ['inflection-template']]]

# @asset
# def filter_and_obtain_df(
#     context: AssetExecutionContext,
#     json_items: List, 
#     ) -> pd.DataFrame:
#     """Filter a list of JSON items by rows, and transform it into a dataframe."""
    
#     logger = get_dagster_logger()

#     # Remove items that don't have "forms" as children
#     filtered_data = [item for item in json_items if "forms" in item]

#     # Convert the filtered data to a dataframe
#     df = pd.json_normalize(filtered_data)

#     df['filtered_forms'] = df['forms'].apply(filter_tags)

#     filter_and_obtain_df = df

#     return filter_and_obtain_df

@asset
def filter_and_obtain_df_all_words(
    context: AssetExecutionContext,
    json_all_words: List, 
    ) -> pd.DataFrame:
    """Filter a list of JSON items by rows, and transform it into a dataframe."""
    
    logger = get_dagster_logger()

    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_all_words if "forms" in item]

    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    df['filtered_forms'] = df['forms'].apply(filter_tags)

    filter_and_obtain_df_all_words = df

    return filter_and_obtain_df_all_words

@asset
def filter_and_obtain_df_verbs(
    context: AssetExecutionContext,
    json_verbs: List, 
    ) -> pd.DataFrame:
    """Filter a list of JSON items by rows, and transform it into a dataframe."""
    
    logger = get_dagster_logger()

    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_verbs if "forms" in item]

    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    df['filtered_forms'] = df['forms'].apply(filter_tags)

    filter_and_obtain_df_verbs = df

    return filter_and_obtain_df_verbs

@asset
def filter_and_obtain_df_adjectives(
    context: AssetExecutionContext,
    json_adjectives: List, 
    ) -> pd.DataFrame:
    """Filter a list of JSON items by rows, and transform it into a dataframe."""
    
    logger = get_dagster_logger()

    # Remove items that don't have "forms" as children
    filtered_data = [item for item in json_adjectives if "forms" in item]

    # Convert the filtered data to a dataframe
    df = pd.json_normalize(filtered_data)

    df['filtered_forms'] = df['forms'].apply(filter_tags)

    filter_and_obtain_df_adjectives = df

    return filter_and_obtain_df_adjectives