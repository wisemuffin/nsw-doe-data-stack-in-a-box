import sys
from pprint import pprint

from dagster import AssetKey

from orchestration.pipeline_nsw_doe import defs

pprint(sys.path)

# from orchestration import pipeline_nsw_doe
# import orchestration


df = defs.load_asset_value(
    AssetKey(["analytics", "metrics_by_year_school_saved_query"])
)

print(df.head())
