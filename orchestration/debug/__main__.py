import os
import sys
from pprint import pprint
from typing import List, Union

from dagster import AssetsDefinition, SourceAsset, materialize
from demo_pipeline_jaffle_shop import all_assets, resources_by_env
from demo_pipeline_jaffle_shop.assets.machine_learning import prophet_forecast

pprint(sys.path)


# this script allows you to run an asset locally without the dagser UI
# Executes a single-threaded, in-process run which materializes provided assets.

resource_defs = resources_by_env[os.getenv("ENV", "dev")]


def is_valid_type(element) -> bool:
    return isinstance(element, AssetsDefinition) or isinstance(element, SourceAsset)


def list_to_typed_list(in_list: List) -> List[Union[AssetsDefinition, SourceAsset]]:
    return list(filter(is_valid_type, in_list))


if __name__ == "__main__":
    # TODO filter all_assets to only the key you need, rather than importing. not urgent
    # x_keys_filt = [x.keys for x in list_to_typed_list( all_assets) if isinstance(x, AssetsDefinition) and "prophet_forecast_model" in x.keys]
    # print(x_keys_filt)

    materialize(
        assets=list_to_typed_list(
            all_assets
        ),  # have to pass in all assets so it know the dependancices
        resources=resource_defs,
        run_config={},
        # partition_key="2024-03-15", #doesnt work - no data example - i.e. if start with this in duckdb then types wont be correct then will fail
        # partition_key="2024-03-17", # works has data
        selection=[
            prophet_forecast.prophet_forecast_transform,
            prophet_forecast.prophet_forecast_model,
            # raw_customers_py
        ],  # only materilise this asset
    )
