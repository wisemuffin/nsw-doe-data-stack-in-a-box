import os

from dagster import Definitions, FilesystemIOManager, load_assets_from_package_module
from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagstermill import ConfigurableLocalOutputNotebookIOManager
from dotenv import load_dotenv

# from dagster_airbyte import airbyte_resource
# from .assets import jaffle_shop_dbt_assets,raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove #,csv_to_onelake_asset
# from .assets import iris,raw,transformation,machine_learning
from . import assets
from .constants import dbt_project_dir, duckdb_project_dir
from .schedules import schedules

load_dotenv()

DEMO_JAFFLE_SHOP_DB_NAME__DEV = os.getenv("DEMO_JAFFLE_SHOP_DB_NAME__DEV")
DEMO_JAFFLE_SHOP_DB_NAME__PROD = os.getenv("DEMO_JAFFLE_SHOP_DB_NAME__PROD")

DB_NAME__DEV = f"{DEMO_JAFFLE_SHOP_DB_NAME__DEV}.duckdb"
DB_NAME__PROD = f"{DEMO_JAFFLE_SHOP_DB_NAME__PROD}.duckdb"

resources_by_env = {
    "prod": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=f"md:{DEMO_JAFFLE_SHOP_DB_NAME__PROD}",
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
    },
    "dev": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=os.path.join(duckdb_project_dir, DB_NAME__DEV)
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
    },
}

# all_assets = [*load_assets_from_package_module(raw, group_name="jaffle_shop"), *load_assets_from_package_module(transformation, group_name="jaffle_shop"), *load_assets_from_package_module(iris, group_name="other"), *load_assets_from_package_module(machine_learning, group_name="jaffle_shop")]
all_assets = load_assets_from_package_module(assets)

defs = Definitions(
    # assets=[raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove,jaffle_shop_dbt_assets],
    assets=all_assets,
    schedules=schedules,
    resources=resources_by_env[os.getenv("DEMO_JAFFLE_SHOP__ENV", "dev")],
)
