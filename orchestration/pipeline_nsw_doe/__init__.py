import time
import os
import re
from pathlib import Path

from dagster import (
    AssetSelection,
    Definitions,
    FilesystemIOManager,
    ScheduleDefinition,
    define_asset_job,
    in_process_executor,
    load_assets_from_package_module,
    EnvVar,
    multi_or_in_process_executor,
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
from . import sensors
from .project import nsw_doe_data_stack_in_a_box_project


load_dotenv()

# work around to set schema when in a branch deployment, DAGSTER_CLOUD_GIT_BRANCH is only present in branch deployments
if "DAGSTER_CLOUD_GIT_BRANCH" in os.environ:
    # Get the current timestamp
    timestamp = int(time.time())
    # pr_string = f"pr_{timestamp}_"
    pr_string = "pr_full_"

    # Get the Git branch (assuming it's an environment variable)
    git_branch = os.environ.get("DAGSTER_CLOUD_GIT_BRANCH", "")
    git_branch_lower = git_branch.lower()

    # Replace non-alphanumeric characters with underscores
    git_branch_clean = re.sub(r"[^a-zA-Z0-9]", "_", git_branch_lower)

    # Final result
    result = pr_string + git_branch_clean
    print(f"setting NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA = {result}")
    os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA"] = result

NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB"
)
DUCKDB_PROJECT_DIR = str(
    Path(__file__).parent.parent.parent.joinpath(
        os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB"]
    )
)

resources_by_env = {
    "prod": {
        "io_manager_dw": DuckDBPandasIOManager(
            database=f"{NSW_DOE_DATA_STACK_IN_A_BOX_DB_PATH_AND_DB}",
        ),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=nsw_doe_data_stack_in_a_box_project),
        "dlt": DagsterDltResource(),
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
        "openai": OpenAIResource(api_key=EnvVar("OPENAI_API_KEY")),
    },
    "dev": {
        "io_manager_dw": DuckDBPandasIOManager(database=DUCKDB_PROJECT_DIR),
        "io_manager": FilesystemIOManager(),
        "dbt": DbtCliResource(project_dir=nsw_doe_data_stack_in_a_box_project),
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
    | AssetSelection.groups("OpenAI_Demo")
)
assets_not_requiring_apis = AssetSelection.all() - assets_requiring_apis

etl_not_requiring_apis = define_asset_job(
    name="etl_not_requiring_apis",
    selection=assets_not_requiring_apis,
    # config={
    #     "execution": {
    #         "config": {
    #             "multiprocess": {
    #                 "max_concurrent": 4,
    #             },
    #         }
    #     }
    # },
)

etl_requiring_apis = define_asset_job(
    name="etl_requiring_apis",
    selection=assets_requiring_apis - AssetSelection.groups("OpenAI_Demo"),
    # config={
    #     "execution": {
    #         "config": {
    #             "multiprocess": {
    #                 "max_concurrent": 4,
    #             },
    #         }
    #     }
    # },
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
    # assets to not be materialized concurrently when running in local dev environments to avoid duckdb limitation of conncurrancy
    # see: https://duckdb.org/docs/connect/concurrency.html
    # when in prod or test env we are using motherduck so no concurrency limitations
    executor=in_process_executor
    if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev") == "dev"
    else multi_or_in_process_executor,
)
