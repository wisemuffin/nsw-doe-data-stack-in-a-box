import os

from dagster import (
    Definitions,
    FilesystemIOManager,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagster_msteams import make_teams_on_run_failure_sensor
from dagstermill import ConfigurableLocalOutputNotebookIOManager
from dotenv import load_dotenv

# from dagster_airbyte import airbyte_resource
# from .assets import jaffle_shop_dbt_assets,raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove #,csv_to_onelake_asset
# from .assets import iris,raw,transformation,machine_learning
from . import assets
from .constants import dbt_project_dir, duckdb_project_dir

load_dotenv()

NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__DEV = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__DEV"
)
NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD"
)
NSW_DOE_DATA_STACK_IN_A_BOX_DB_TOKEN__PROD = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_DB_TOKEN__PROD"
)

DB_NAME__DEV = f"{NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__DEV}.duckdb"
DB_NAME__PROD = f"{NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD}.duckdb"

resources_by_env = {
    "prod": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=f"md:{NSW_DOE_DATA_STACK_IN_A_BOX_DB_NAME__PROD}?motherduck_token={NSW_DOE_DATA_STACK_IN_A_BOX_DB_TOKEN__PROD}",
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

all_assets_job = define_asset_job(
    name="etl_job",
    # selection=all_assets,
    config={
        "execution": {
            "config": {
                "multiprocess": {
                    "max_concurrent": 4,
                },
            }
        }
    },
)

msteams_on_run_failure = make_teams_on_run_failure_sensor(
    hook_url="",
    monitored_jobs=([all_assets_job]),
)

schedule_all_asset_job = ScheduleDefinition(
    job=all_assets_job, cron_schedule="0 0 * * *"
)

# schedule_dbt_assets =  build_schedule_from_dbt_selection(
#         [jaffle_shop_dbt_assets],
#         job_name="materialize_dbt_models",
#         cron_schedule="0 0 * * *",
#         dbt_select="fqn:*",
#     )

defs = Definitions(
    assets=all_assets,
    resources=resources_by_env[os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev")],
    jobs=[all_assets_job],
    schedules=[schedule_all_asset_job],
    sensors=[msteams_on_run_failure],
)
