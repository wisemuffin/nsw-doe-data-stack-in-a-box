import os
from pathlib import Path

# from dagster import file_relative_path
from dagster_dbt import DbtCliResource

# DBT_MANIFEST_PATH = file_relative_path(__file__, "../../dbt/target/manifest.json")

# dbt_project_dir = Path(__file__).joinpath(home, "cese-dai-analytics", "dbt").resolve()


# dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "transformation","transformation_nsw_doe").resolve()
dbt_project_dir = os.path.join(
    os.environ["GITHUB_WORKSPACE"],
    os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR"],
)
dbt = DbtCliResource(project_dir=dbt_project_dir)

dbt_manifest_path_temp = os.path.join(dbt_project_dir, "target", "manifest.json")


# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.


if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD") or not os.path.exists(
    dbt_manifest_path_temp
):
    dbt_parse_invocation = dbt.cli(
        ["parse"]
    ).wait()  # dbt_parse_invocation = dbt.cli(["parse"]).wait()
    # dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")	    # # dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")
    dbt_manifest_path = dbt_parse_invocation.target_path.joinpath(
        "manifest.json"
    )  # dbt_manifest_path = dbt_parse_invocation.target_path.joinpath( "manifest.json")
    # dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")	    # # dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")

    dbt_manifest_path = (
        dbt.cli(  # working around this issue: https://github.com/dagster-io/dagster/discussions/18235
            ["--quiet", "parse"], target_path=Path("target")
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = os.path.join(dbt_project_dir, "target", "manifest.json")
