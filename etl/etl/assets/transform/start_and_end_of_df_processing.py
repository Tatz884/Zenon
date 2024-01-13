from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)
from typing import List, Tuple

import pandas as pd

"""
Edit this file for changing the dependency of df import/export
"""


@asset
def start_process_df(
    context: AssetExecutionContext,
    filter_and_obtain_df_all_words: pd.DataFrame, 
    ) -> pd.DataFrame:
    """Just copies the df made by filter_and_obtain_df_series.
    Change the dependency of this function - this function provides one-stop entry point for transform process.
    """
    
    logger = get_dagster_logger()

    df = filter_and_obtain_df_all_words

    start_process_df = df

    context.add_output_metadata(
        metadata={
            "num_records": len(start_process_df),  # Metadata can be any key-value pair
            "whole_df_preview": MetadataValue.md(df.head().to_markdown()),
            "forms_preview": MetadataValue.md(start_process_df.forms.head().to_markdown()),
            # "nested_forms_preview": MetadataValue.md(transform_df.nested_forms.head().to_markdown()),
            # "invalid_forms": MetadataValue.md(transform_df.invalid_forms.head().to_markdown()),
            # "invalid_forms_percents": MetadataValue.md(transform_df.invalid_forms_percent.head().to_markdown()),
            # "invalid_forms_percent_average": MetadataValue.float(transform_df.invalid_forms_percent.mean()),
        }
    )

    
    return start_process_df

@asset
def finish_process_df(
    context: AssetExecutionContext,
    start_process_df: pd.DataFrame,
    get_json_from_df: pd.DataFrame,
    get_glosses_df: pd.Series,
    get_flattened_forms_df: pd.Series
    ) -> pd.DataFrame:
    """Transform a row-filtered dataframe into a dataframe with additional columns
    and without extraneous columns."""
    
    # convert pd.Series to pd.DataFrame.
    get_glosses_df = get_glosses_df.to_frame("glosses")
    get_flattened_forms_df = get_flattened_forms_df.to_frame('flattened_forms')

    # horizontally concatenate all df.
    df = pd.concat([start_process_df, get_json_from_df, get_glosses_df, get_flattened_forms_df], axis=1)
    df = df.sort_values(by='invalid_forms_percent', ascending=False)
    finish_process_df = df

    context.add_output_metadata(
        metadata={
            "num_records": len(finish_process_df),  # Metadata can be any key-value pair
            "whole_df_preview": MetadataValue.md(df.head().to_markdown()),
            "nest_forms_preview": MetadataValue.md(df.nest_forms.head().to_markdown()),
            "invalid_forms_in_nest_forms": MetadataValue.md(df.invalid_forms_in_nest_forms.head().to_markdown()),
            "invalid_forms_percents": MetadataValue.md(df.invalid_forms_percent.head().to_markdown()),
            "invalid_forms_percent_average": MetadataValue.float(df.invalid_forms_percent.mean()),
        }
    )

    finish_process_df = finish_process_df[['word', 'pos', 'lang', 'glosses', 'json_forms', 'flattened_forms']]

    print(finish_process_df)
    return finish_process_df

