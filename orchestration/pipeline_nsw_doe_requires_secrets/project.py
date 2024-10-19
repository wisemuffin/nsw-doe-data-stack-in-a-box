import os
from pathlib import Path

from dagster_dbt import DbtProject


project_dir = (
    Path(__file__)
    .joinpath(
        "..", "..", "..", os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR"]
    )
    .resolve()
)

nsw_doe_data_stack_in_a_box_project = DbtProject(
    project_dir=project_dir,
    packaged_project_dir=Path(__file__).joinpath("..", "dbt-project-temp").resolve(),
)
nsw_doe_data_stack_in_a_box_project.prepare_if_dev()
