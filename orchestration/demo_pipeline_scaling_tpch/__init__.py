import os
from pathlib import Path

from dagster import Definitions, FilesystemIOManager, load_assets_from_package_module
from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagstermill import ConfigurableLocalOutputNotebookIOManager
from dotenv import load_dotenv

# from dagster_airbyte import airbyte_resource
# from .assets import jaffle_shop_dbt_assets,raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove #,csv_to_onelake_asset
# from .assets import iris,raw,transformation,machine_learning
from . import assets
from .project import tpch_project
from .schedules import schedules

from .util.branching import set_schema_name_env

load_dotenv()


set_schema_name_env()

TPCH_TARGET_SCHEMA = os.getenv("TPCH_TARGET_SCHEMA")


TPCH_DB_PATH_AND_DB = os.getenv("TPCH_DB_PATH_AND_DB")
DUCKDB_PROJECT_DIR = str(
    Path(__file__).parent.parent.parent.joinpath(os.environ["TPCH_DB_PATH_AND_DB"])
)

S3_BUCKET_METADATA = os.getenv("S3_BUCKET_METADATA")

TPCH__ENV = os.getenv("TPCH__ENV", "dev")

resources_by_env = {
    "prod": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=f"{TPCH_DB_PATH_AND_DB}",
        ),
        # "io_manager": S3PickleIOManager(
        #     s3_resource=S3Resource(),
        #     s3_bucket=f"{S3_BUCKET_METADATA}",
        #     s3_prefix=f"{TPCH_TARGET_SCHEMA}",
        # ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=tpch_project),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
    },
    "test": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=f"{TPCH_DB_PATH_AND_DB}",
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=tpch_project),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
    },
    "dev": {
        "io_manager_dw": DuckDBPandasIOManager(database=DUCKDB_PROJECT_DIR),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=tpch_project),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
    },
}

# all_assets = [*load_assets_from_package_module(raw, group_name="TPCH"), *load_assets_from_package_module(transformation, group_name="TPCH"), *load_assets_from_package_module(iris, group_name="other"), *load_assets_from_package_module(machine_learning, group_name="TPCH")]
all_assets = load_assets_from_package_module(assets)

defs = Definitions(
    # assets=[raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove,TPCH_dbt_assets],
    assets=all_assets,
    schedules=schedules,
    resources=resources_by_env[os.getenv("TPCH__ENV", "dev")],
)
