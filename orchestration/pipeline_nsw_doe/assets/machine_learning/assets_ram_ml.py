import base64
from io import BytesIO

import pandas as pd
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetOut,
    MetadataValue,
    Output,
    asset,
    multi_asset,
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    PredictionErrorDisplay,
)
from sklearn.linear_model import LinearRegression


import numpy as np


@asset(
    group_name="machine_learning__resource_allocation_model",
    ins={"metrics_by_year_school_saved_query": AssetIn(key_prefix=["analytics"])},
)
def preprocess_dataset(
    context: AssetExecutionContext, metrics_by_year_school_saved_query: pd.DataFrame
):
    """This function preprocess the dataset to be used in the model"""

    # # example of how to substitute

    features = [
        "school__latest_year_enrolment_fte",
        "school__level_of_schooling",
        "school__icsea_value",
        "school__selective_school",
        "school__school_specialty_type",
    ]
    target = "funding_aud_original"

    preprocess_dataset = metrics_by_year_school_saved_query[[*features, target]]

    preprocess_dataset = pd.get_dummies(preprocess_dataset)

    preprocess_dataset = preprocess_dataset.dropna()  # yolo

    # ideally should also do more preprocessing ... scaling, getdummies ect. # lazy

    return preprocess_dataset


@multi_asset(
    outs={"training_data": AssetOut(), "test_data": AssetOut()},
    group_name="machine_learning__resource_allocation_model",
)
def create_train_test_data(
    context: AssetExecutionContext, preprocess_dataset: pd.DataFrame
):
    """This function will create the train data by segmenting the dataset"""
    # df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    # X = df.drop("col1")
    # y = df["col2"]

    target = "funding_aud_original"
    preprocess_dataset["funding_aud_original"]
    X = preprocess_dataset.drop(target, axis=1)
    y = preprocess_dataset[target]
    # Split the dataset to reserve 20% of records as the test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    training_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    return training_data, test_data


@multi_asset(
    outs={"train_model_baseline": AssetOut(), "importance": AssetOut()},
    group_name="machine_learning__resource_allocation_model",
)
def train_model_baseline(
    context: AssetExecutionContext, training_data: pd.DataFrame, test_data: pd.DataFrame
):
    """Function to train the Linear Regression model

    Args:
        training_data (pd.DataFrame): the training dataset

    Returns:
        model (LinearRegression): the fitted model
    """

    # model training
    context.log.info("     Training the model...\n")
    X, y = training_data.iloc[:, :-1], training_data.iloc[:, -1]
    train_model_baseline = LinearRegression().fit(X, y)

    context.log.info(f"\n    {train_model_baseline}, is trained!")

    importance_dict = {
        "Features": X.columns,
        "Importance": train_model_baseline.coef_[0],
        "Importance_abs": np.abs(train_model_baseline.coef_[0]),
    }
    importance = pd.DataFrame(importance_dict).sort_values(
        by="Importance", ascending=True
    )

    yield Output(train_model_baseline, output_name="train_model_baseline")
    yield Output(importance, output_name="importance")


# @asset(group_name="machine_learning__resource_allocation_model")
# def train_model_baseline_test_set_r_squared(test_data, train_model_baseline: LinearRegression):
#     transformed_X_test, transformed_y_test = transformed_test_data
#     score = train_model_baseline.score()


@asset(group_name="machine_learning__resource_allocation_model")
def predictions(test_data: pd.DataFrame, train_model_baseline: LinearRegression):
    """Function to forecast the test dataset

    Args:
        test_data (pd.DataFrame): the test dataset
        train_model_baseline (LinearRegression): the fitted model

    Returns:
        forecast (pd.DataFrame): the forecasted dataset
    """
    print("     Forecasting the test dataset...")
    X, _y = test_data.iloc[:, :-1], test_data.iloc[:, -1]

    predictions = train_model_baseline.predict(X)
    print("     Forecasting done!")
    return predictions


@asset(group_name="machine_learning__resource_allocation_model")
def create_metrics(
    predictions, test_data: pd.DataFrame, train_model_baseline: LinearRegression
):
    print("     Creating the metrics...")

    # test the model
    _X_test, y_test = test_data.iloc[:, :-1], test_data.iloc[:, -1]
    # r_squared = train_model_baseline.score(X_test,y_test)

    # y_pred = train_model_baseline.predict(X_test)
    y_pred = predictions

    # plot predictions - should refactor
    plot = PredictionErrorDisplay.from_predictions(
        y_test,
        y_pred,
        kind="actual_vs_predicted",
        # ax=ax0,
        scatter_kwargs={"alpha": 0.5},
    )
    buffer = BytesIO()
    plot.figure_.savefig(buffer)
    image_data = base64.b64encode(buffer.getvalue())
    pred_vs_test_graph = MetadataValue.md(
        f"![img](data:image/png;base64,{image_data.decode()})"
    )

    metadata = {}
    metadata["score (mean_absolute_error)"] = float(mean_absolute_error(y_test, y_pred))
    metadata["score (mean_squared_error)"] = float(mean_squared_error(y_test, y_pred))
    metadata["score (r2_score)"] = float(r2_score(y_test, y_pred))
    metadata["pred vs test plot"] = pred_vs_test_graph

    metrics = {"score (mean_absolute_error)": metadata["score (mean_absolute_error)"]}

    return Output(metrics, metadata=metadata)
