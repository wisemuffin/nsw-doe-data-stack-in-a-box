import pandas as pd
from dagster import AssetIn, asset, file_relative_path, Field, Int
from dagstermill import define_dagstermill_asset


metrics_by_year_school_saved_query = define_dagstermill_asset(
    name="forecasting",
    notebook_path=file_relative_path(__file__, "../../notebooks/data-science-example.ipynb"),
    ins={"metrics_by_year_school_saved_query": AssetIn(key_prefix=["analytics"])},
    group_name="machine_learning",
    # group_name="ML",
    config_schema=Field(
        Int,
        default_value=3,
        is_required=False,
        description="The number of clusters to find",
    ),
)