import pandas as pd
from dagster import AssetIn, Field, Int, asset, file_relative_path
from dagstermill import define_dagstermill_asset


@asset(compute_kind="python", io_manager_key="io_manager_dw", group_name="Iris")
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


iris_kmeans_jupyter_notebook_finished = define_dagstermill_asset(
    name="iris_kmeans_jupyter_finished",
    notebook_path=file_relative_path(__file__, "../../notebooks/iris-kmeans.ipynb"),
    ins={"iris": AssetIn("iris_dataset")},
    group_name="Iris",
    config_schema=Field(
        Int,
        default_value=3,
        is_required=False,
        description="The number of clusters to find",
    ),
)
