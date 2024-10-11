import os
from pathlib import Path

from dagster_dbt import DbtProject, DbtCliResource


project_dir = (
    Path(__file__)
    .joinpath(
        "..", "..", "..", os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR"]
    )
    .resolve()
)


dbt = DbtCliResource(project_dir=str(project_dir))

if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD") or not os.path.exists(
    os.path.join(project_dir, "target")
):
    dbt.cli(["deps"]).wait()
    dbt_parse_invocation = dbt.cli(["parse"]).wait()


nsw_doe_data_stack_in_a_box_project = DbtProject(
    project_dir=project_dir,
    packaged_project_dir=Path(__file__).joinpath("..", "dbt-project-temp").resolve(),
)
