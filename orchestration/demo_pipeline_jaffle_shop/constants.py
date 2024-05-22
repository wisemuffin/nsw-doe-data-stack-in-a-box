import os
from pathlib import Path

# from dagster import file_relative_path
from dagster_dbt import DbtCliResource

# DBT_MANIFEST_PATH = file_relative_path(__file__, "../../dbt/target/manifest.json")

# home = os.environ['HOME']

# dbt_project_dir = Path(__file__).joinpath(home, "cese-dai-analytics", "dbt").resolve()


# dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "transformation", "demo_transformation_jaffle_shop").resolve()
# duckdb_project_dir = Path(__file__).joinpath("..", "..", "..", "reports", "sources", "demo_transformation_jaffle_shop").resolve()
dbt_project_dir = Path(os.environ["DEMO_JAFFLE_SHOP_DBT_PROJECT_DIR"])
duckdb_project_dir = Path(os.environ["DEMO_JAFFLE_SHOP_DB_PATH__DEV"])
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

dbt_manifest_path_temp = dbt_project_dir.joinpath("target", "manifest.json")


# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.


if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD") or not os.path.exists(
    dbt_manifest_path_temp
):
    dbt_parse_invocation = dbt.cli(["parse"]).wait()
    # dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")
