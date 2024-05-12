import pandas as pd
from dagster import AssetExecutionContext, AssetIn, AssetOut, asset, multi_asset
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import roc_auc_score


import numpy as np


# # example of getting dagster asset when developing locally
# from orchestration.pipeline_nsw_doe import defs
# metrics_by_year_school_saved_query = defs.load_asset_value(AssetKey(['analytics','metrics_by_year_school_saved_query']))


@multi_asset(
    ins={"metrics_by_year_school_saved_query": AssetIn(key_prefix=["analytics"])},
    outs={"training_data_demo": AssetOut(), "test_data_demo": AssetOut()},
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


@asset(
    group_name="ml_dg",
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

    return preprocess_dataset


@multi_asset(
    outs={"training_data": AssetOut(), "test_data": AssetOut()}, group_name="ml_dg"
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
    group_name="ml_dg",
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
    return train_model_baseline, importance


# @asset(group_name="ml_dg")
# def train_model_baseline_test_set_r_squared(test_data, train_model_baseline: LinearRegression):
#     transformed_X_test, transformed_y_test = transformed_test_data
#     score = train_model_baseline.score()


@asset(group_name="ml_dg")
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


# @asset(group_name="ml_dg")
# def create_metrics(predictions:np.array, test_data:np.array, auc_score):
#     print("     Creating the metrics...")
#     threshold = 0.5
#     threshold_vector = np.greater_equal(predictions, threshold).astype(int)

#     y_test = test_data.iloc[:,-1]

#     mae = mean_absolute_error(y_test,y_pred)
#     mape = mean_absolute_percentage_error(y_test,y_pred)
#     mse = mean_squared_error(y_test,y_pred)


#     dict_ftpn = {"tp": true_positive, "tn": true_negative, "fp": false_positive, "fn": false_negative}


#     metrics = {"f1_score": f1_score,
#                "accuracy": accuracy,
#                "auc_score": auc_score,
#                "dict_ftpn": dict_ftpn,
#                'number_of_predictions': len(predictions),
#                'number_of_good_predictions':number_of_good_predictions,
#                'number_of_false_predictions':number_of_false_predictions}

#     return metrics
