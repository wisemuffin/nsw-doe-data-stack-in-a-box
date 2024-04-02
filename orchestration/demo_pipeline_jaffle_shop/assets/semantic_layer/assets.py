import os
import subprocess

from dagster_dbt import get_asset_key_for_model
import pandas as pd
from dagster import AssetIn, asset, file_relative_path, Field, Int, load_assets_from_package_module
from metricflow.cli.main import cli as mf

from ...constants import dbt_project_dir
from ..transformation import jaffle_shop_dbt_assets


@asset(compute_kind="python",io_manager_key="io_manager_dw", key_prefix=["analytics"], group_name="semantic_layer", deps=[get_asset_key_for_model([jaffle_shop_dbt_assets],'orders'), get_asset_key_for_model([jaffle_shop_dbt_assets],'customers')])
def sml_orders() -> pd.DataFrame:
    """runs: mf query --saved-query orders_saved_query --csv ./orders-saved-query.csv"""

    # csv_location = './exports/orders-saved-query.csv'
    csv_location = os.path.join(dbt_project_dir, "exports","orders-saved-query.csv")

    working_dir = dbt_project_dir
    # command = ["pwd"]
    command = ['mf', 'query', '--saved-query', 'orders_saved_query', '--csv', csv_location]
    subprocess.check_call(command, cwd=working_dir)

    # TODO refactor variables
    df = pd.read_csv(csv_location)

    # print(df.to_markdown())
    return df


