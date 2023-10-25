from dagster import (
    Definitions,
    load_assets_from_modules,
    FilesystemIOManager,
)

from .assets import extract, transform, load

all_assets = load_assets_from_modules([extract, transform, load])

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": io_manager,
    }
)
