import os
import sys
from pprint import pprint

from dagster import materialize, DailyPartitionsDefinition

pprint(sys.path)

from demo_pipeline_jaffle_shop import resources_by_env
from demo_pipeline_jaffle_shop.assets import raw_orders_py, raw_customers_py

# this script allows you to run an asset locally without the dagser UI
# Executes a single-threaded, in-process run which materializes provided assets.

resource_defs = resources_by_env[os.getenv("ENV", "dev")]

if __name__ == "__main__":
    sources = [] #[sourceA.to_source_asset(), *source_multi_asset.to_source_assets()]
    materialize(assets=[
                    raw_orders_py
                    # raw_customers_py
                    ] 
                    + sources,
                partition_key="2024-01-14", #works
                # partition_key="2024-03-17", # no data example
                resources=resource_defs,
                run_config={})