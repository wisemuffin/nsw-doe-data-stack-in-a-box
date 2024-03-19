import pandas as pd
from dagster import AssetExecutionContext, asset, DailyPartitionsDefinition, file_relative_path
from typing import Union


@asset(compute_kind="python", key_prefix=["raw"],io_manager_key="io_manager_dw")
def raw_customers_py() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_customers.csv"
    df =pd.read_csv(
        url,
    )

    df['_load_timestamp'] = pd.Timestamp('now')
    df['_source'] = url

    return df

@asset(compute_kind="python", key_prefix=["raw"], partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"), metadata={"partition_expr": "order_date"},io_manager_key="io_manager_dw")
def raw_orders_py(context: AssetExecutionContext) -> Union[pd.DataFrame,None]:
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv"
    # input_dtype = {
    #     'id': 'int64',
    #     'user_id': 'int64',
    #     # 'order_date': 'datetime64[ns]', # TypeError: the dtype datetime64 is not supported for parsing, pass this column using parse_dates instead
    #     'status': 'string' 
    # }
    output_dtype = {
        'id': 'int64',
        'user_id': 'int64',
        'order_date': 'datetime64[ns]',
        'status': 'string', 
        # '_load_datetime': 'datetime64[ns]',
        '_source': 'string'
    }
    df = pd.read_csv(
        url,
        parse_dates=['order_date'] # TypeError: the dtype datetime64 is not supported for parsing, pass this column using parse_dates instead
    )

    # df['_load_timestamp'] = pd.Timestamp('now') # partions no longer working with load timestamp TODO
    df['_source'] = url

    df['order_date'] = df['order_date']  + pd.offsets.DateOffset(years=6)

    df_partition = df[df.order_date.dt.strftime('%Y-%m-%d') == context.asset_partition_key_for_output()]

    ## workaround pandas data type datetime64[ns] to pyarrow giving erros. so just change to date
    # df_partition['order_date'] =  pd.to_datetime(df_partition['order_date'] ).dt.date

    if df_partition.empty:
        context.log.info("No data returned. Skipping asset creation.")
        df_none = df_partition.astype(output_dtype, errors='raise')
        context.log.info(f'data types for df_none: \n{df_none.dtypes}')
        # TODO limitation pandas to duckdb io manager when recieves empty df then it wont use the dtypes from dataframe 
        # when building db objects. i.e. strings are getting convereted to int32...
        return df_none
    else:
        return df_partition

@asset(compute_kind="python", key_prefix=["raw"],io_manager_key="io_manager_dw")
def raw_payments_py() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_payments.csv"
    df = pd.read_csv(
        url,
    )
    df['_load_timestamp'] = pd.Timestamp('now')
    df['_source'] = url
    return df