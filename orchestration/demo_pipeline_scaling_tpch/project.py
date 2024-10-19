import os
from pathlib import Path

from dagster_dbt import DbtProject, DbtCliResource


project_dir = (
    Path(__file__)
    .joinpath("..", "..", "..", os.environ["TPCH_DBT_PROJECT_DIR"])
    .resolve()
)


dbt = DbtCliResource(project_dir=str(project_dir))

tpch_project = DbtProject(
    project_dir=project_dir,
    packaged_project_dir=Path(__file__).joinpath("..", "dbt-project-temp").resolve(),
)
tpch_project.prepare_if_dev()
