import pandas as pd
import datetime

from typing import Any
from dagster import AssetIn, FreshnessPolicy, MetadataValue, asset, file_relative_path
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from dagster_dbt import get_asset_key_for_model

from demo_pipeline_jaffle_shop.assets import transformation

@asset(
    ins={"orders": AssetIn(key_prefix=["analytics"])},
    compute_kind="python",
    # group_name="machine_learning_prophet_forecast",
    io_manager_key="io_manager_dw"
)
def prophet_forecast_transform(context, orders: pd.DataFrame) -> Any:
    """Model parameters that best fit the observed data"""
    df = orders
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
    df_grouped = (
        df[["order_date", "amount"]]
        .groupby(by="order_date", as_index=False)
        .sum()
    )
    # print(df_grouped.head())

    # rename columns to be used by prophet
    df_grouped.rename(
        columns={"order_date": "ds", "amount": "y"}, inplace=True
    )

    return df_grouped


@asset(
    compute_kind="python",
    # group_name="machine_learning_prophet_forecast",
    io_manager_key="io_manager"
)
def prophet_forecast_model(
    context, prophet_forecast_transform: pd.DataFrame
) -> Prophet:
    m = Prophet()
    m.fit(prophet_forecast_transform)
    return m


@asset(
    compute_kind="python",
    # group_name="machine_learning_prophet_forecast",
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=120),
    io_manager_key="io_manager"
)
def prophet_forecast_predict(
    context, prophet_forecast_model: Prophet, prophet_forecast_transform: pd.DataFrame
) -> Any:
    n_future_days = 30
    ds = prophet_forecast_transform["ds"].max()
    future_dates = []
    for _ in range(n_future_days):
        ds = ds + datetime.timedelta(days=1)
        future_dates.append(ds)

    df_future = pd.DataFrame({"ds": future_dates})
    forecast = prophet_forecast_model.predict(df_future)

    return forecast


@asset(
    compute_kind="python",
    # group_name="machine_learning_prophet_forecast",
    io_manager_key="io_manager"
)
def prophet_forecast_model_plot(
    context, prophet_forecast_predict: pd.DataFrame, prophet_forecast_model: Prophet
) -> Any:
    forecast = prophet_forecast_predict
    fig = plot_plotly(
        prophet_forecast_model,
        forecast,
        xlabel="order date",
        ylabel="order amount",
    )
    # fig.write_image("my_forecast_plot.png")
    save_chart_path = file_relative_path(
        __file__, "./temp_vis/prophet_forecast_chart.html"
    )
    fig.write_html(save_chart_path, auto_open=True)
    context.add_output_metadata(
        {
            "plot_url": MetadataValue.url("file://" + save_chart_path),
        }
    )


@asset(
    compute_kind="python",
    # group_name="machine_learning_prophet_forecast",
    io_manager_key="io_manager"
)
def prophet_forecast_model_plot_components(
    context, prophet_forecast_predict: pd.DataFrame, prophet_forecast_model: Prophet
) -> Any:
    forecast = prophet_forecast_predict
    fig_components = plot_components_plotly(prophet_forecast_model, forecast)

    save_chart_components_path = file_relative_path(
        __file__, "./temp_vis/prophet_forecast_components_chart.html"
    )

    fig_components.write_html(save_chart_components_path, auto_open=True)

    context.add_output_metadata(
        {
            "plot_components_url": MetadataValue.url(
                "file://" + save_chart_components_path
            ),
        }
    )
