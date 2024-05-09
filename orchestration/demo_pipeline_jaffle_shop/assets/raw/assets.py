from typing import Union

import pandas as pd
from dagster import (
    AssetCheckResult,
    AssetCheckSpec,
    AssetExecutionContext,
    AssetKey,
    DailyPartitionsDefinition,
    Output,
    asset,
)


@asset(
    compute_kind="python",
    key_prefix=["raw"],
    io_manager_key="io_manager_dw",
    check_specs=[
        AssetCheckSpec(
            name="raw_customers_py_id_has_no_nulls",
            asset=AssetKey(["raw", "raw_customers_py"]),
        )
    ],
)
def raw_customers_py():
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_customers.csv"
    df = pd.read_csv(
        url,
    )

    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url

    # return Output(df, metadata={"num_rows": df.shape[0]})

    yield Output(df, metadata={"num_rows": df.shape[0]})

    # checks
    count_nulls = df["id"].isna().sum()
    yield AssetCheckResult(passed=bool(count_nulls == 0))


# @asset_check(asset=raw_customers_py)
# def num_rows_is_within_two_standard_deviations(context: AssetExecutionContext):
#     records = context.instance.get_event_records(
#         EventRecordsFilter(DagsterEventType.ASSET_MATERIALIZATION, asset_key=AssetKey("raw_customers_py")),
#         limit=11,
#     )

#     num_rows_values = [
#         record.asset_materialization.metadata["num_rows"].value for record in records
#     ]
#     mean = statistics.mean(num_rows_values[:-1])
#     stdev = statistics.stdev(num_rows_values[:-1])

#     return AssetCheckResult(passed=abs(num_rows_values[-1] - mean) - 2 * stdev)

# @asset_check(asset=raw_customers_py)
# def no_null_event_ids(context: AssetExecutionContext, raw_customers_py):
#     count_nulls = raw_customers_py['id'].isna().sum()
#     return AssetCheckResult(passed=count_nulls == 0)


@asset(compute_kind="python", key_prefix=["raw"], io_manager_key="io_manager_dw")
def raw_orders_py(context: AssetExecutionContext) -> Union[pd.DataFrame, None]:
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv"
    df = pd.read_csv(
        url,
        parse_dates=[
            "order_date"
        ],  # TypeError: the dtype datetime64 is not supported for parsing, pass this column using parse_dates instead
    )

    # df['_load_timestamp'] = pd.Timestamp('now') # partions no longer working with load timestamp TODO
    df["_source"] = url

    df["order_date"] = df["order_date"] + pd.offsets.DateOffset(years=6)
    return df


@asset(
    compute_kind="python",
    key_prefix=["raw"],
    partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"),
    metadata={"partition_expr": "order_date"},
    io_manager_key="io_manager_dw",
)
def raw_orders_partitioned_py(
    context: AssetExecutionContext,
) -> Union[pd.DataFrame, None]:
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv"
    # input_dtype = {
    #     'id': 'int64',
    #     'user_id': 'int64',
    #     # 'order_date': 'datetime64[ns]', # TypeError: the dtype datetime64 is not supported for parsing, pass this column using parse_dates instead
    #     'status': 'string'
    # }
    output_dtype = {
        "id": "int64",
        "user_id": "int64",
        "order_date": "datetime64[ns]",
        "status": "string",
        # '_load_datetime': 'datetime64[ns]',
        "_source": "string",
    }
    df = pd.read_csv(
        url,
        parse_dates=[
            "order_date"
        ],  # TypeError: the dtype datetime64 is not supported for parsing, pass this column using parse_dates instead
    )

    # df['_load_timestamp'] = pd.Timestamp('now') # partions no longer working with load timestamp TODO
    df["_source"] = url

    df["order_date"] = df["order_date"] + pd.offsets.DateOffset(years=6)

    df_partition = df[
        df.order_date.dt.strftime("%Y-%m-%d")
        == context.asset_partition_key_for_output()
    ]

    ## workaround pandas data type datetime64[ns] to pyarrow giving erros. so just change to date
    # df_partition['order_date'] =  pd.to_datetime(df_partition['order_date'] ).dt.date

    if df_partition.empty:
        context.log.info("No data returned. Skipping asset creation.")
        df_none = df_partition.astype(output_dtype, errors="raise")
        context.log.info(f"data types for df_none: \n{df_none.dtypes}")
        # TODO limitation pandas to duckdb io manager when recieves empty df then it wont use the dtypes from dataframe
        # when building db objects. i.e. strings are getting convereted to int32...
        return df_none
    else:
        return df_partition


@asset(compute_kind="python", key_prefix=["raw"], io_manager_key="io_manager_dw")
def raw_payments_py() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_payments.csv"
    df = pd.read_csv(
        url,
    )
    df["_load_timestamp"] = pd.Timestamp("now")
    df["_source"] = url
    return df
