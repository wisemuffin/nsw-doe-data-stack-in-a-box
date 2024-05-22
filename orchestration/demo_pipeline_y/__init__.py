from dagster import (
    Definitions,
    asset,
)


@asset
def my_asset_1():
    return [1, 2, 3]


@asset
def my_asset_2():
    return [1, 2, 3]


defs = Definitions(
    assets=[my_asset_1, my_asset_2],
)
