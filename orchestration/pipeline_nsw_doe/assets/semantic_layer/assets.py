import os
import subprocess
from pathlib import Path

import tempfile
import pandas as pd
from dagster import Output, asset, AssetExecutionContext
from dagster_dbt import get_asset_key_for_model

from ...project import nsw_doe_data_stack_in_a_box_project
from ..transformation import nsw_doe_dbt_assets


@asset(
    compute_kind="python",
    io_manager_key="io_manager_dw",
    key_prefix=["analytics"],
    group_name="semantic_layer",
    deps=[
        get_asset_key_for_model([nsw_doe_dbt_assets], "fct__resource_allocation"),
        get_asset_key_for_model([nsw_doe_dbt_assets], "fct__staff"),
        get_asset_key_for_model([nsw_doe_dbt_assets], "fct__student"),
        get_asset_key_for_model([nsw_doe_dbt_assets], "fct__school"),
        get_asset_key_for_model([nsw_doe_dbt_assets], "dim__date"),
    ],
)
def metrics_by_year_saved_query(context: AssetExecutionContext):
    # import re
    # import sys
    # from metricflow.cli.main import cli
    # if __name__ == "__main__":
    #     sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    #     sys.exit(cli())

    working_dir = nsw_doe_data_stack_in_a_box_project.project_dir

    command = ["dbt", "docs", "generate"]
    subprocess.check_call(command, cwd=working_dir)

    context.log.info(f"cwd: {Path.cwd()}")
    context.log.info(f"working_dir: {working_dir}")

    tmp = tempfile.NamedTemporaryFile()

    context.log.info(f"tmp: {tmp}")

    # Open the file for writing.
    with open(tmp.name, "w") as f:
        f.write("stuff")  # where `stuff` is, y'know... stuff to write (a string)

    ...

    # Open the file for reading.
    with open(tmp.name) as f:
        for line in f:
            context.log.info(f"line: {line}")
            ...  # more things here

    with tempfile.TemporaryDirectory() as tmpdirname:
        context.log.info(f"created temporary directory: {tmpdirname}")
        csv_location = os.path.join(
            tmpdirname,
            "sq-metrics-by-year-saved-query.csv",
        )
        context.log.info(f"csv_location: {csv_location}")

        command = [
            "mf",
            "query",
            "--saved-query",
            "metrics_by_year_saved_query",
            "--csv",
            csv_location,
        ]
        subprocess.check_call(command, cwd=working_dir)

        # TODO refactor variables
        df = pd.read_csv(csv_location, parse_dates=["metric_time__year"])

    # 🚧 TODO: fixing data types manually. Dont like this but ok for demos
    # df['metric_time__year'] = pd.to_datetime(df['metric_time__year']).dt.strftime('%Y-%m-%d')
    df["funding_aud_post_adjustments"] = df["funding_aud_post_adjustments"].astype(
        pd.Int64Dtype()
    )

    # print(df.dtypes)
    yield Output(df, metadata={"num_rows": df.shape[0]})


@asset(
    compute_kind="python",
    io_manager_key="io_manager_dw",
    key_prefix=["analytics"],
    group_name="semantic_layer",
    deps=[
        get_asset_key_for_model([nsw_doe_dbt_assets], "fct__resource_allocation"),
        get_asset_key_for_model([nsw_doe_dbt_assets], "dim__school"),
        get_asset_key_for_model([nsw_doe_dbt_assets], "dim__date"),
    ],
)
def metrics_by_year_school_saved_query(context: AssetExecutionContext):
    csv_location = os.path.join(
        nsw_doe_data_stack_in_a_box_project.project_dir,
        "exports",
        "sq-metrics-by-year-school-saved-query.csv",
    )

    working_dir = nsw_doe_data_stack_in_a_box_project.project_dir

    context.log.info(f"working_dir: {working_dir}")
    context.log.info(f"csv_location: {csv_location}")

    command = ["dbt", "docs", "generate"]
    subprocess.check_call(command, cwd=working_dir)

    command = [
        "mf",
        "query",
        "--saved-query",
        "metrics_by_year_school_saved_query",
        "--csv",
        csv_location,
    ]
    subprocess.check_call(command, cwd=working_dir)

    # TODO refactor variables
    df = pd.read_csv(csv_location, parse_dates=["metric_time__year"])

    # 🚧 TODO: fixing data types manually. Dont like this but ok for demos
    # df['metric_time__year'] = pd.to_datetime(df['metric_time__year']).dt.strftime('%Y-%m-%d')
    df["funding_aud_post_adjustments"] = df["funding_aud_post_adjustments"].astype(
        pd.Int64Dtype()
    )

    # print(df.dtypes)
    yield Output(df, metadata={"num_rows": df.shape[0]})
