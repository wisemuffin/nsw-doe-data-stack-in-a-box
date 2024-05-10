import pandas as pd
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetOut,
    multi_asset,
)
from sklearn.model_selection import train_test_split


@multi_asset(
    ins={"metrics_by_year_school_saved_query": AssetIn(key_prefix=["analytics"])},
    outs={"training_data": AssetOut(), "test_data": AssetOut()},
)
def training_test_data(
    context: AssetExecutionContext, metrics_by_year_school_saved_query: pd.DataFrame
):
    # df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    # X = df.drop("col1")
    # y = df["col2"]

    features = [
        "school__latest_year_enrolment_fte",
        "school__level_of_schooling",
        "school__icsea_value",
        "school__selective_school",
        "school__school_specialty_type",
    ]
    X = metrics_by_year_school_saved_query[
        metrics_by_year_school_saved_query.columns.intersection(features)
    ]
    y = metrics_by_year_school_saved_query["funding_aud_original"]
    # Split the dataset to reserve 20% of records as the test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return (X_train, y_train), (X_test, y_test)
