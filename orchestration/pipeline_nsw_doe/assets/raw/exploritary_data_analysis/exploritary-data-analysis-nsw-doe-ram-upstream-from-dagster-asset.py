import sys
from pprint import pprint

from dagster import AssetKey
import pandas as pd

from orchestration.pipeline_nsw_doe import defs

pprint(sys.path)

# from orchestration import pipeline_nsw_doe
# import orchestration


df: pd.DataFrame = defs.load_asset_value(
    AssetKey(["analytics", "metrics_by_year_school_saved_query"])
)  # type: ignore

df.head()
