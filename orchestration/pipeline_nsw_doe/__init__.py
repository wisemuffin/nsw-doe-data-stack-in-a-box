import os

from dagster import (
    AssetSelection,
    Definitions,
    FilesystemIOManager,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
    EnvVar,
)
from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagster_msteams import make_teams_on_run_failure_sensor
from dagstermill import ConfigurableLocalOutputNotebookIOManager
from dotenv import load_dotenv
from dagster_openai import OpenAIResource

from dagster_embedded_elt.dlt import DagsterDltResource


# from dagster_airbyte import airbyte_resource
# from .assets import jaffle_shop_dbt_assets,raw_customers_py,raw_orders_py,raw_payments_py,iris_dataset,iris_dataset_test_to_remove #,csv_to_onelake_asset
# from .assets import iris,raw,transformation,machine_learning
from . import assets
from .constants import dbt_project_dir
from . import sensors

load_dotenv()

NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB"
)
DUCKDB_PROJECT_DIR = os.path.join(
    os.environ["GITHUB_WORKSPACE"],
    os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB"],
)

resources_by_env = {
    "prod": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=f"{NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB}",
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        "dlt": DagsterDltResource(),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
        "openai": OpenAIResource(api_key=EnvVar("OPENAI_API_KEY")),
    },
    "dev": {
        "io_manager_dw": DuckDBPandasIOManager(database=DUCKDB_PROJECT_DIR),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        "dlt": DagsterDltResource(),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
        "openai": OpenAIResource(api_key=EnvVar("OPENAI_API_KEY")),
    },
}

all_assets = load_assets_from_package_module(assets)


# filtered_assets = [asset for asset in all_assets if ((isinstance(asset, AssetsDefinition) and ("raw" in asset.get_attributes_dict().get("group_names_by_key", {})))) ]# and ("raw_google" in asset.group_names_by_key or "raw_github" in asset.group_names_by_key or "requires_api" in asset.group_names_by_key)))]

assets_requiring_apis = (
    AssetSelection.groups("raw_google_analytics")
    | AssetSelection.groups("raw_github")
    | AssetSelection.groups("transformation_requires_api")
)
assets_not_requiring_apis = AssetSelection.all() - assets_requiring_apis

etl_not_requiring_apis = define_asset_job(
    name="etl_not_requiring_apis",
    selection=assets_not_requiring_apis,
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

etl_requiring_apis = define_asset_job(
    name="etl_requiring_apis",
    selection=assets_requiring_apis,
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
    monitored_jobs=([etl_requiring_apis]),
)


schedule_etl_requiring_apis = ScheduleDefinition(
    job=etl_requiring_apis, cron_schedule="0 0 * * *"
)

schedule_etl_not_requiring_apis = ScheduleDefinition(
    job=etl_not_requiring_apis, cron_schedule="0 1 * * *"
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
    jobs=[etl_requiring_apis, etl_not_requiring_apis],
    schedules=[schedule_etl_requiring_apis, schedule_etl_not_requiring_apis],
    sensors=[msteams_on_run_failure, sensors.question_sensor],
)
