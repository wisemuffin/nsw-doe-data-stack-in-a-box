from typing import Union

import pandas as pd
import pandera as pa
from dagster import AssetCheckResult, AssetCheckSpec, AssetExecutionContext, AssetKey, DagsterEventType, EventRecordsFilter, Output, asset, DailyPartitionsDefinition, MonthlyPartitionsDefinition, asset_check, file_relative_path

from pipeline_nsw_doe.factory import pandera_schema_to_dagster_type
from .schema_masterdataset import schema as schema_masterdataset
from .schema_ram import schema as schema_ram


DatahubMasterDatasetDagsterType = pandera_schema_to_dagster_type(
    schema=schema_masterdataset, 
    name="DatahubMasterDatasetDagsterType", 
    description="data frame DagsterType type for this dummy asset."
)


@asset(compute_kind="python", key_prefix=["raw"], group_name="raw_datahub",io_manager_key="io_manager_dw", dagster_type=DatahubMasterDatasetDagsterType, check_specs=[AssetCheckSpec(name="raw__nsw_doe_datahub__master_dataset_id_has_no_nulls", asset=AssetKey(['raw', 'raw__nsw_doe_datahub__master_dataset']))])
def raw__nsw_doe_datahub__master_dataset():
    url = "https://data.cese.nsw.gov.au/data/dataset/027493b2-33ad-3f5b-8ed9-37cdca2b8650/resource/2ac19870-44f6-443d-a0c3-4c867f04c305/download/master_dataset.csv"
    df =pd.read_csv(
        url,
    )

    df['_load_timestamp'] = pd.Timestamp('now')
    df['_source'] = url

    df.head()
    print(df.shape)
    print(df.dtypes)

    # schema = pa.infer_schema(df)
    # schema_script = schema.to_script('schema_template.py')
    # print(schema_script)

    yield Output(df, metadata={"num_rows": df.shape[0]})

    # checks
    count_nulls = df['School_code'].isna().sum()
    yield AssetCheckResult(passed=bool(count_nulls == 0))


DatahubRamDagsterType = pandera_schema_to_dagster_type(
    schema=schema_ram, 
    name="DatahubRamDagsterType", 
    description="data frame DagsterType type for this dummy asset."
)

@asset(compute_kind="python", key_prefix=["raw"],io_manager_key="io_manager_dw", group_name="raw_datahub", dagster_type=DatahubRamDagsterType, check_specs=[AssetCheckSpec(name="raw__nsw_doe_datahub__ram_id_has_no_nulls", asset=AssetKey(['raw', 'raw__nsw_doe_datahub__ram']))])
def raw__nsw_doe_datahub__ram():
    url_dict = {}
    url_dict["2024"] = "https://data.cese.nsw.gov.au/data/dataset/e354d699-2b59-3ef0-9477-ee63289d7466/resource/2776c893-71d5-4fc5-a64a-848507c22cc5/download/data-hub-2024-sbar-1.csv"
    url_dict["2023"] = "https://data.cese.nsw.gov.au/data/dataset/e354d699-2b59-3ef0-9477-ee63289d7466/resource/649adcc8-221d-47a7-924e-499c16b416c3/download/data-hub-2023-approved-ram.csv"
    url_dict["2022"] = "https://data.cese.nsw.gov.au/data/dataset/e354d699-2b59-3ef0-9477-ee63289d7466/resource/a7efba8f-fb18-4442-8ddd-f98fd330b997/download/data-hub-2022-approved-ram.csv"
    url_dict["2021"] = "https://data.cese.nsw.gov.au/data/dataset/e354d699-2b59-3ef0-9477-ee63289d7466/resource/2ac4e49f-6da4-4bcf-910a-5e08e7dff5f2/download/data-hub-2021-approved-ram.csv"
    url_dict["2020"] = "https://data.cese.nsw.gov.au/data/dataset/e354d699-2b59-3ef0-9477-ee63289d7466/resource/882e5421-0e40-418b-a3b6-db25c1b8f004/download/data-hub-2020-approved-ram.csv"
    url_dict["2019"] = "https://data.cese.nsw.gov.au/data/dataset/e354d699-2b59-3ef0-9477-ee63289d7466/resource/b2a2b1de-3e46-43a6-929e-2ba65ab3fad5/download/data-hub-2019-approved.csv"
    
    df_ram_all_years = pd.DataFrame({})

    for year in url_dict.keys():

        df_per_year =pd.read_csv(
            url_dict[year],
        )

        df_per_year['year'] = year
        df_per_year['_load_timestamp'] = pd.Timestamp('now')
        df_per_year['_source'] = url_dict[year]


        df_ram_all_years = pd.concat([df_ram_all_years, df_per_year])
    


    # some rows are none
    # df_ram_all_years[df_ram_all_years["School Code"].isna()]

    # fixing up picking total rows from CSVs
    df_ram_all_years = df_ram_all_years.dropna(subset=["School Code"])


    df_ram_all_years.head()
    df_ram_all_years['School Code'].isna().sum()
    


    yield Output(df_ram_all_years, metadata={"num_rows": df_ram_all_years.shape[0]})

    # checks
    count_nulls = df_ram_all_years['School Code'].isna().sum()
    yield AssetCheckResult(passed=bool(count_nulls == 0))



@asset(compute_kind="python", key_prefix=["raw"], group_name="raw_acara",io_manager_key="io_manager_dw")
def raw__acara__staff_numbers():
    url = "https://dataandreporting.blob.core.windows.net/anrdataportal/ANR-ExcelDownloads/2022R1/Staff%20numbers%20dataset.xlsx"
    df =pd.read_excel(
        url,
    )

    df['_load_timestamp'] = pd.Timestamp('now')
    df['_source'] = url


    yield Output(df, metadata={"num_rows": df.shape[0]})


@asset(compute_kind="python", key_prefix=["raw"], group_name="raw_acara",io_manager_key="io_manager_dw")
def raw__acara__student_numbers():
    url = "https://dataandreporting.blob.core.windows.net/anrdataportal/ANR-ExcelDownloads/2022R1/Student%20numbers%20dataset.xlsx"
    df =pd.read_excel(
        url,
    )

    df['_load_timestamp'] = pd.Timestamp('now')
    df['_source'] = url

    yield Output(df, metadata={"num_rows": df.shape[0]})



# %%
