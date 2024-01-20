from dagster import (
    Definitions,
    load_assets_from_modules,
    load_assets_from_package_module,
    get_dagster_logger,
    FilesystemIOManager,
    AssetSelection,
    define_asset_job
)

from etl.assets import extract, transform, load, inspect

logger = get_dagster_logger()

extract_assets = load_assets_from_package_module(extract, group_name="extract")
transform_assets = load_assets_from_package_module(transform, group_name="transform")
load_assets = load_assets_from_package_module(load, group_name="load")
inspect_assets = load_assets_from_package_module(inspect, group_name="inspect")

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

# To make a job,
# select the following assets:
# 1. json_all_words
# 2. the assets downstream of json_all_words and also in transform group
# 3. load_into_cockroachDB_dev
selection_all_words_crDB_dev = AssetSelection.keys("json_all_words") | \
(AssetSelection.groups("transform") & AssetSelection.keys("json_all_words").downstream()) | \
AssetSelection.keys("load_into_cockroachDB_dev") \



defs = Definitions(
    assets =
    extract_assets + 
    transform_assets +
    load_assets +
    inspect_assets, # concatenate two lists
    jobs = [define_asset_job("load_all_words_into_crDB_dev", selection=selection_all_words_crDB_dev)],

    resources={
        "io_manager": io_manager,
    }
)
