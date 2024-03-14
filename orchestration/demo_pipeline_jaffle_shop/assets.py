import pandas as pd
from dagster import AssetExecutionContext, asset, DailyPartitionsDefinition, file_relative_path
from dagster_dbt import DbtCliResource, dbt_assets

from .constants import dbt_manifest_path
# from .example_onelake_resource import OnelakeResource

@dbt_assets(manifest=dbt_manifest_path)
def jaffle_shop_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(compute_kind="python", key_prefix=["raw"])
def raw_customers_py() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_customers.csv",
    )

@asset(compute_kind="python", key_prefix=["raw"], partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"), metadata={"partition_expr": "order_date"})
def raw_orders_py(context: AssetExecutionContext) -> pd.DataFrame:
    df = pd.read_csv(
        "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv",
        parse_dates=['order_date'] # having some trouble with default timestamp to ns with pyarrow
    )

    df['order_date'] = df['order_date']  + pd.offsets.DateOffset(years=6)

    df_partition = df[df.order_date.dt.strftime('%Y-%m-%d') == context.asset_partition_key_for_output()]

    ## workaround pandas data type datetime64[ns] to pyarrow giving erros. so just change to date
    df_partition['order_date'] =  pd.to_datetime(df_partition['order_date'] ).dt.date


    return df_partition

@asset(compute_kind="python", key_prefix=["raw"])
def raw_payments_py() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_payments.csv",
    )




@asset(compute_kind="python")
def iris_dataset() -> pd.DataFrame:
    return pd.read_csv(
        "https://docs.dagster.io/assets/iris.csv",
        names=[
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
            "species",
        ],
    )

@asset(compute_kind="python")
def iris_dataset_test_to_remove() -> pd.DataFrame:
    return pd.read_csv(
        "https://docs.dagster.io/assets/iris.csv",
        names=[
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
            "species",
        ],
    )

# @asset
# def csv_to_onelake_asset(onelake_td_dia: OnelakeResource) -> None:
#     df = pd.DataFrame([{"dave":55}])
#     onelake_td_dia.upload_df_to_csv_fabric(df=df, file_name="df_to_fabric.csv")
#     return None

if __name__ == '__main__':
    raw_orders_py()
