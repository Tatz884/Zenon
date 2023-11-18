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
###### get_flattened_forms_df ######

@asset
def get_flattened_forms_df(
    context: AssetExecutionContext,
    start_process_df: pd.DataFrame, 
) -> pd.Series:
    logger = get_dagster_logger()

    df = start_process_df

    get_flattened_forms_df = df.forms.apply(lambda x: [item['form'] for item in x])

    return get_flattened_forms_df
