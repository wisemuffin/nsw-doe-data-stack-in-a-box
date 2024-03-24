import os

from dotenv import load_dotenv

from dagster import Definitions, FilesystemIOManager, load_assets_from_package_module
from dagster_dbt import DbtCliResource

from dagster_dbt import dbt_cli_resource
from dagster_duckdb_pandas import duckdb_pandas_io_manager, DuckDBPandasIOManager
# from dagster_airbyte import airbyte_resource

# from .assets import jaffle_shop_dbt_assets,raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove #,csv_to_onelake_asset
from .assets import other,raw,transformation,machine_learning
from .constants import dbt_project_dir, duckdb_project_dir
from .schedules import schedules

load_dotenv()

NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__DEV = os.getenv('NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__DEV')
NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD = os.getenv('NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD')

DB_NAME__DEV = f"{NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__DEV}.duckdb"
DB_NAME__PROD = f"{NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD}.duckdb"

resources_by_env = {
    "prod": {
        "io_manager_dw": DuckDBPandasIOManager(
                database=  f'md:{NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD}',
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir))
    },
    "dev": {
        "io_manager_dw": DuckDBPandasIOManager(
                database= os.path.join(
                    duckdb_project_dir, DB_NAME__DEV
                )
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir))
    },
}

all_assets = [*load_assets_from_package_module(raw, group_name="jaffle_shop"), *load_assets_from_package_module(transformation, group_name="jaffle_shop"), *load_assets_from_package_module(other, group_name="other"), *load_assets_from_package_module(machine_learning, group_name="jaffle_shop")]

defs = Definitions(
    # assets=[raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove,jaffle_shop_dbt_assets],
    assets=all_assets,
    schedules=schedules,
    resources=resources_by_env[os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev")],
)