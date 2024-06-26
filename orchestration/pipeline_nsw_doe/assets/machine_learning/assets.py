import pandas as pd
from dagster import (
    AssetExecutionContext,
    AssetIn,
    Field,
    Int,
    asset,
    file_relative_path,
)
from dagstermill import define_dagstermill_asset

metrics_by_year_school_saved_query = define_dagstermill_asset(
    name="forecasting",
    notebook_path=file_relative_path(
        __file__, "../../notebooks/data-science-example.ipynb"
    ),
    ins={"metrics_by_year_school_saved_query": AssetIn(key_prefix=["analytics"])},
    group_name="machine_learning__demo_notebooks",
    # group_name="ML",
    config_schema=Field(
        Int,
        default_value=3,
        is_required=False,
        description="The number of clusters to find",
    ),
)


@asset(
    ins={"metrics_by_year_school_saved_query": AssetIn(key_prefix=["analytics"])},
    compute_kind="pandas",
    group_name="machine_learning__demo_notebooks",
)
def example_ml_for_testing(
    context: AssetExecutionContext, metrics_by_year_school_saved_query: pd.DataFrame
) -> pd.DataFrame:
    context.log.info(metrics_by_year_school_saved_query.head())
    return metrics_by_year_school_saved_query
