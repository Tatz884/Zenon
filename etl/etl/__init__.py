from dagster import (
    Definitions,
    load_assets_from_modules,
    load_assets_from_package_module,
    get_dagster_logger,
    FilesystemIOManager,

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

defs = Definitions(
    assets =
    extract_assets + 
    transform_assets +
    load_assets +
    inspect_assets, # concatenate two lists

    resources={
        "io_manager": io_manager,
    }
)
