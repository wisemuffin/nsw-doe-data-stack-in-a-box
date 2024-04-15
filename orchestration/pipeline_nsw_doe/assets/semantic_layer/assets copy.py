import os

import subprocess
from pathlib import Path, PurePath

from dagster_dbt import get_asset_key_for_model
import pandas as pd
from dagster import AssetIn, asset, file_relative_path, Field, Int, load_assets_from_package_module
from metricflow.cli.main import cli as mf


dbt_project_dir = Path( os.environ['NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR'])
duckdb_project_dir = Path( os.environ['NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH__DEV'])


def sq__resource_allocation() -> pd.DataFrame:
    """runs: mf query --saved-query resource_allocation_saved_query --csv ./exports/saved_query__resource-allocation.csv"""

    # csv_location = './exports/resource-allocation.csv'
    csv_location = os.path.join(dbt_project_dir, "exports","sq-resource-allocation.csv")

    working_dir = dbt_project_dir
    # command = ["pwd"]
    command = ['mf', 'query', '--saved-query', 'resource_allocation_saved_query', '--csv', csv_location]
    subprocess.check_call(command, cwd=working_dir)

    # TODO refactor variables
    df = pd.read_csv(csv_location)

    print(df.dtypes)
    # print(df.to_markdown())
    return df


sq__resource_allocation()

