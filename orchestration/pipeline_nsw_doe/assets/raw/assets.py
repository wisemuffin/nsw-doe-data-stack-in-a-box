import os

import pandas as pd
from dagster import (
    AssetCheckResult,
    AssetCheckSpec,
    AssetKey,
    Output,
    asset,
)

from dagster_pandera import pandera_schema_to_dagster_type
# from pipeline_nsw_doe.factory import pandera_schema_to_dagster_type

from .schema_masterdataset import schema as schema_masterdataset
from .schema_ram import schema as schema_ram

DatahubMasterDatasetDagsterType = pandera_schema_to_dagster_type(
    schema=schema_masterdataset
)

NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA: str = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA", "schema_not_set"
)


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_datahub",
    io_manager_key="io_manager_dw",
    dagster_type=DatahubMasterDatasetDagsterType,
    check_specs=[
        AssetCheckSpec(
            name="raw__nsw_doe_datahub__master_dataset_id_has_no_nulls",
            asset=AssetKey(
                [
                    NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,
                    "raw__nsw_doe_datahub__master_dataset",
                ]
            ),
        )
    ],
)
def raw__nsw_doe_datahub__master_dataset():
    url = "https://data.nsw.gov.au/data/dataset/78c10ea3-8d04-4c9c-b255-bbf8547e37e7/resource/3e6d5f6a-055c-440d-a690-fc0537c31095/download/master_dataset.csv"
    df = pd.read_csv(
        url,
        # on_bad_lines="skip",  # 🚧 TODO Temp workaround due to malformed csv
    )

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    df.head()
    print(df.shape)
    print(df.dtypes)

    # df = df.head(100)  # 🚧 TODO - temp fix to skip errors with malformed csv

    # schema = pa.infer_schema(df)
    # schema_script = schema.to_script('schema_template.py')
    # print(schema_script)

    yield Output(df, metadata={"num_rows": df.shape[0]})

    # checks
    count_nulls = df["School_code"].isna().sum()
    yield AssetCheckResult(passed=bool(count_nulls == 0))


DatahubRamDagsterType = pandera_schema_to_dagster_type(
    schema=schema_ram,
)


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    io_manager_key="io_manager_dw",
    group_name="raw_datahub",
    dagster_type=DatahubRamDagsterType,
    check_specs=[
        AssetCheckSpec(
            name="raw__nsw_doe_datahub__ram_id_has_no_nulls",
            asset=AssetKey(
                [NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA, "raw__nsw_doe_datahub__ram"]
            ),
        )
    ],
)
def raw__nsw_doe_datahub__ram():
    url_dict = {}
    url_dict["2024"] = (
        "https://data.nsw.gov.au/data/dataset/3ea5010a-89bd-46bf-be2a-13c82cc0e1bb/resource/44e8373b-a006-4e02-a7ab-f012270b1528/download/data-hub-2024-sbar-adjustments.csv"
    )
    url_dict["2023"] = (
        "https://data.nsw.gov.au/data/dataset/3ea5010a-89bd-46bf-be2a-13c82cc0e1bb/resource/1487bf5f-2ae8-40c0-a9ad-5ff442228a45/download/data-hub-2023-approved-ram.csv"
    )
    url_dict["2022"] = (
        "https://data.nsw.gov.au/data/dataset/3ea5010a-89bd-46bf-be2a-13c82cc0e1bb/resource/1c5a3e63-0c57-4a6e-8b9c-cace158de065/download/data-hub-2022-approved-ram.csv"
    )
    url_dict["2021"] = (
        "https://data.nsw.gov.au/data/dataset/3ea5010a-89bd-46bf-be2a-13c82cc0e1bb/resource/8df93694-7307-40c3-aa1d-86b918361dfc/download/data-hub-2021-approved-ram.csv"
    )
    url_dict["2020"] = (
        "https://data.nsw.gov.au/data/dataset/3ea5010a-89bd-46bf-be2a-13c82cc0e1bb/resource/e827169d-8ac0-4a3f-ae29-c648d1761611/download/data-hub-2020-approved-ram.csv"
    )
    url_dict["2019"] = (
        "https://data.nsw.gov.au/data/dataset/3ea5010a-89bd-46bf-be2a-13c82cc0e1bb/resource/15087669-9982-4255-9e8a-b46a58ad9067/download/data-hub-2019-approved.csv"
    )

    df_ram_all_years = pd.DataFrame({})

    for year in url_dict.keys():
        df_per_year = pd.read_csv(
            url_dict[year],
        )

        df_per_year["year"] = int(year)
        df_per_year["_load_timestamp"] = pd.Timestamp("now")
        df_per_year["_source"] = url_dict[year]

        df_ram_all_years = pd.concat([df_ram_all_years, df_per_year])

    # some rows are none
    # df_ram_all_years[df_ram_all_years["School Code"].isna()]

    # fixing up picking total rows from CSVs
    df_ram_all_years = df_ram_all_years.dropna(subset=["School Code"])

    df_ram_all_years.head()
    df_ram_all_years["School Code"].isna().sum()

    yield Output(df_ram_all_years, metadata={"num_rows": df_ram_all_years.shape[0]})

    # checks
    count_nulls = df_ram_all_years["School Code"].isna().sum()
    yield AssetCheckResult(passed=bool(count_nulls == 0))


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_datahub",
    io_manager_key="io_manager_dw",
    check_specs=[
        AssetCheckSpec(
            name="raw__nsw_doe_datahub__attendance_id_has_no_nulls",
            asset=AssetKey(
                [
                    NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,
                    "raw__nsw_doe_datahub__attendance",
                ]
            ),
        )
    ],
)
def raw__nsw_doe_datahub__attendance():
    url = "https://data.nsw.gov.au/data/dataset/b558a070-09f5-4941-a140-e60a744327bf/resource/df5e3989-0595-4c61-94ab-0f63ab6b1528/download/2023-attendance-rates-by-government-schools.csv"
    df = pd.read_csv(
        url,
    )

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    df.head()
    print(df.shape)
    print(df.dtypes)

    yield Output(df, metadata={"num_rows": df.shape[0]})

    # checks
    count_nulls = df["school_code"].isna().sum()
    yield AssetCheckResult(passed=bool(count_nulls == 0))


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_datahub",
    io_manager_key="io_manager_dw",
)
def raw__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals():
    url = "https://data.nsw.gov.au/data/dataset/f7cba3fc-6e9b-4b8b-b1fd-e7dda9b49001/resource/54d2df2f-44ae-4d67-980f-ce855d68f2d5/download/apprenticeship_traineeship_training_contract_approvals-1.xlsx"
    df = pd.read_excel(url, sheet_name="Training Type", header=3)

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    df.head()
    print(df.shape)
    print(df.dtypes)

    yield Output(df, metadata={"num_rows": df.shape[0]})


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_datahub",
    io_manager_key="io_manager_dw",
)
def raw__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions():
    url = "https://data.nsw.gov.au/data/dataset/f7cba3fc-6e9b-4b8b-b1fd-e7dda9b49001/resource/e969d98e-d89a-474b-b89b-9452f1e45644/download/apprenticeship_traineeship_training_contract_completions.xlsx"
    df = pd.read_excel(url, sheet_name="Training Type", header=3)

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    df.head()
    print(df.shape)
    print(df.dtypes)

    yield Output(df, metadata={"num_rows": df.shape[0]})


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_datahub",
    io_manager_key="io_manager_dw",
)
def raw__nsw_doe_datahub__apprenticeship_traineeship_training_contract_in_training():
    url = "https://data.nsw.gov.au/data/dataset/f7cba3fc-6e9b-4b8b-b1fd-e7dda9b49001/resource/fe7169bf-32ba-433b-8354-eb9ef5477eaa/download/apprenticeship_traineeship_training_contract_in-trainings.xlsx"
    df = pd.read_excel(url, sheet_name="Training Type", header=3)

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    df.head()
    print(df.shape)
    print(df.dtypes)

    yield Output(df, metadata={"num_rows": df.shape[0]})


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_acara",
    io_manager_key="io_manager_dw",
)
def raw__acara__staff_numbers():
    url = "https://dataandreporting.blob.core.windows.net/anrdataportal/ANR-ExcelDownloads/2022R1/Staff%20numbers%20dataset.xlsx"
    df = pd.read_excel(
        url,
    )

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    yield Output(df, metadata={"num_rows": df.shape[0]})


@asset(
    compute_kind="python",
    key_prefix=[NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA],
    group_name="raw_acara",
    io_manager_key="io_manager_dw",
)
def raw__acara__student_numbers():
    url = "https://dataandreporting.blob.core.windows.net/anrdataportal/ANR-ExcelDownloads/2022R1/Student%20numbers%20dataset.xlsx"
    df = pd.read_excel(
        url,
    )

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    yield Output(df, metadata={"num_rows": df.shape[0]})
