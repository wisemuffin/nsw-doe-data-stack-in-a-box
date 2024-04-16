import os
import subprocess

from dagster_dbt import get_asset_key_for_model
import pandas as pd
from dagster import AssetIn, asset, file_relative_path, Field, Int, load_assets_from_package_module
from metricflow.cli.main import cli as mf

from ...constants import dbt_project_dir
from ..transformation import jaffle_shop_dbt_assets


@asset(compute_kind="python",io_manager_key="io_manager_dw", key_prefix=["analytics"], group_name="semantic_layer", deps=[get_asset_key_for_model([jaffle_shop_dbt_assets],'fct__resource_allocation'), get_asset_key_for_model([jaffle_shop_dbt_assets],'fct__staff')])
def metrics_by_year_saved_query() -> pd.DataFrame:

    csv_location = os.path.join(dbt_project_dir, "exports","sq-metrics-by-year-saved-query.csv")

    working_dir = dbt_project_dir
    command = ['mf', 'query', '--saved-query', 'metrics_by_year_saved_query', '--csv', csv_location]
    subprocess.check_call(command, cwd=working_dir)

    # TODO refactor variables
    df = pd.read_csv(csv_location, parse_dates=['metric_time__year'])

    # 🚧 TODO: fixing data types manually. Dont like this but ok for demos
    # df['metric_time__year'] = pd.to_datetime(df['metric_time__year']).dt.strftime('%Y-%m-%d')
    df['funding_aud_post_adjustments'] = df['funding_aud_post_adjustments'].astype(pd.Int64Dtype())

    # print(df.dtypes)
    return df

@asset(compute_kind="python",io_manager_key="io_manager_dw", key_prefix=["analytics"], group_name="semantic_layer", deps=[get_asset_key_for_model([jaffle_shop_dbt_assets],'fct__resource_allocation'),get_asset_key_for_model([jaffle_shop_dbt_assets],'dim__school')])
def metrics_by_year_school_saved_query() -> pd.DataFrame:

    csv_location = os.path.join(dbt_project_dir, "exports","sq-metrics-by-year-school-saved-query.csv")

    working_dir = dbt_project_dir
    command = ['mf', 'query', '--saved-query', 'metrics_by_year_school_saved_query', '--csv', csv_location]
    subprocess.check_call(command, cwd=working_dir)

    # TODO refactor variables
    df = pd.read_csv(csv_location, parse_dates=['metric_time__year'])

    # 🚧 TODO: fixing data types manually. Dont like this but ok for demos
    # df['metric_time__year'] = pd.to_datetime(df['metric_time__year']).dt.strftime('%Y-%m-%d')
    df['funding_aud_post_adjustments'] = df['funding_aud_post_adjustments'].astype(pd.Int64Dtype())

    # print(df.dtypes)
    return df


