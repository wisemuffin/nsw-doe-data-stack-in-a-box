import os
from pathlib import Path

from dagster_dbt import DbtProject


nsw_doe_data_stack_in_a_box_project = DbtProject(
    project_dir=Path(__file__)
    .joinpath(
        "..", "..", "..", os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR"]
    )
    .resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "dbt-project-temp").resolve(),
)
