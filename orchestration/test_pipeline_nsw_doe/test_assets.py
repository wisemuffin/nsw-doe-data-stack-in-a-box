import pandas as pd
from dagster import build_asset_context
from pipeline_nsw_doe.assets.machine_learning import (
    example_ml_for_testing,
)


def test_example_ml_for_testing():
    df = pd.DataFrame(
        [
            {
                "title": "Wow, Dagster is such an awesome and amazing product. I can't wait to use it!"
            },
            {"title": "Pied Piper launches new product"},
        ]
    )
    results = example_ml_for_testing(build_asset_context(), df)
    assert results is not None  # It didnt returned something
