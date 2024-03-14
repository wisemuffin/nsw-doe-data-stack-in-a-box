import os

from dotenv import load_dotenv

from dagster import Definitions, FilesystemIOManager
from dagster_dbt import DbtCliResource

from dagster_dbt import dbt_cli_resource
from dagster_duckdb_pandas import duckdb_pandas_io_manager
# from dagster_airbyte import airbyte_resource

from .assets import jaffle_shop_dbt_assets,raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove #,csv_to_onelake_asset
from .constants import dbt_project_dir, duckdb_project_dir
from .schedules import schedules

load_dotenv()

DOE_NSW_DATA_STACK_IN_A_BOX_DB_NAME__DEV = os.getenv('DOE_NSW_DATA_STACK_IN_A_BOX_DB_NAME__DEV')
DOE_NSW_DATA_STACK_IN_A_BOX_DB_NAME__PROD = os.getenv('DOE_NSW_DATA_STACK_IN_A_BOX_DB_NAME__PROD')

DB_NAME__DEV = f"{DOE_NSW_DATA_STACK_IN_A_BOX_DB_NAME__DEV}.duckdb"
DB_NAME__PROD = f"{DOE_NSW_DATA_STACK_IN_A_BOX_DB_NAME__PROD}.duckdb"

resources_by_env = {
    "prod": {
        "io_manager": duckdb_pandas_io_manager.configured(
            {
                "database": os.path.join(
                    duckdb_project_dir, DB_NAME__PROD
                ),
            }
        ),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir))
    },
    "dev": {
        "io_manager": duckdb_pandas_io_manager.configured(
            {
                "database": os.path.join(
                    duckdb_project_dir, DB_NAME__DEV
                )
            }
        ),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir))
    },
}

defs = Definitions(
    assets=[raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove,jaffle_shop_dbt_assets],
    schedules=schedules,
    resources=resources_by_env[os.getenv("DOE_NSW_DATA_STACK_IN_A_BOX__ENV", "dev")],
)