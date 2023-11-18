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
###### dataframe_to_records ######

@asset
def dataframe_to_records(
    context: AssetExecutionContext,
    finish_process_df: pd.DataFrame
    ) -> List:
    """Convert DataFrame to a list of records, converting the "forms" column to JSON."""
    logger = get_dagster_logger()

    # must be in the order of the database used later
    finish_process_df = finish_process_df[['word', 'pos', 'glosses', 'json_forms', 'flattened_forms', 'lang']]

    records = finish_process_df.reset_index().to_records(index=False)

    # This will include the index name as the first column
    columns = ['index'] + list(finish_process_df.columns)
    dataframe_to_records = [
        tuple(
            json.dumps(record[col], ensure_ascii=False) if col == "forms" else record[col]
            for col in columns
        )
        for record in records
    ]

    context.add_output_metadata(
        metadata={
            "dataframe_info": MetadataValue.md(finish_process_df.head(3).to_markdown()),  # Metadata can be any key-value pair
        }
    )



    return dataframe_to_records