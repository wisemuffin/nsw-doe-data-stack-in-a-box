from typing import Any, Tuple

import numpy as np
import pandas as pd
from dagster import AssetIn, FreshnessPolicy, asset
from scipy import optimize


def model_func(x, a, b):
    return a * np.exp(b * (x / 10**18 - 1.6095))


@asset(
    compute_kind="python",
    # group_name="machine_learning_simple_forecast",
    io_manager_key="io_manager",
    ins={"orders": AssetIn(key_prefix=["analytics"])},
)
# @asset(compute_kind="python")
def simple_forecast_order_model(context, orders: pd.DataFrame) -> Any:
    """Model parameters that best fit the observed data"""
    df = orders
    return tuple(
        optimize.curve_fit(
            f=model_func,
            xdata=df.order_date.astype(np.int64),
            ydata=df.amount,
            # p0=[10, 100],
        )[0]
    )


@asset(
    compute_kind="python",
    # group_name="machine_learning_simple_forecast",
    ins={"orders": AssetIn(key_prefix=["analytics"])},
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=60),
    io_manager_key="io_manager",
)
# @asset(compute_kind="python")
def simple_forecast_predicted_orders(
    orders: pd.DataFrame, simple_forecast_order_model: Tuple[float, float]
) -> pd.DataFrame:
    """Predicted orders for the next 30 days based on the fit paramters"""
    a, b = simple_forecast_order_model
    start_date = orders.order_date.max()
    future_dates = pd.date_range(
        start=start_date, end=start_date + pd.DateOffset(days=30)
    )
    predicted_data = model_func(x=future_dates.astype(np.int64), a=a, b=b)
    return pd.DataFrame({"order_date": future_dates, "amount": predicted_data})
