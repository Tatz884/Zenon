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


@asset
def get_json_from_df(
    context: AssetExecutionContext,
    map_by_tag_apply: pd.DataFrame, 
    ) -> pd.DataFrame:
    """Transform a row-filtered dataframe into a dataframe with additional columns
    and without extraneous columns."""
    
    logger = get_dagster_logger()

    df = map_by_tag_apply

    # df['json_forms'] = df['nest_forms'].apply(lambda x: json.dumps(x, ensure_ascii=False, indent=2)) 
    df['json_forms'] = df['map_by_tag'].apply(lambda x: json.dumps(x, ensure_ascii=False, indent=2)) 

    df['header_sizes'] = df['header_sizes'].apply(lambda x: json.dumps(x, ensure_ascii=False, indent=2)) 

    context.add_output_metadata(
        metadata={
            "num_records": df.info(),  # Metadata can be any key-value pair
            "whole_df_preview": MetadataValue.md(df.head(3).to_markdown()),
            "json_forms_preview": MetadataValue.md(df.json_forms.head(3).to_markdown()),
        }
    )
    get_json_from_df = df

    return get_json_from_df