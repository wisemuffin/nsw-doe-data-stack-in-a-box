from dagster_ge.factory import ge_data_context, ge_validation_op_factory
import pandas as pd
from dagster import asset, AssetIn, AssetOut, AssetMaterialization, MetadataValue, multi_asset



# @asset
# def ge_test():
#     return pd.DataFrame({"cola":[1,2,3]})

@asset
def payroll_read_in_datafile():
    # return pd.read_csv(csv_path)
    return pd.DataFrame({"cola":[1,2,3]})

def process_payroll(df) -> int:
    return len(df)

def postprocess_payroll(numrows, expectation):
    if expectation["success"]:
        return numrows
    else:
        raise ValueError

payroll_expectations = ge_validation_op_factory(
    name="ge_validation_op",
    datasource_name="getest",
    suite_name="basic.warning"
)



@multi_asset(
    ins={"df": AssetIn(key="payroll_read_in_datafile")},
    outs={"payroll_data": AssetOut(),"numrows": AssetOut()}
)
def payroll_data(df):
    numrows = process_payroll(df)
    expectation_result = payroll_expectations(df)
    postprocess_payroll(numrows, expectation_result)
    yield AssetMaterialization(
        asset_key="payroll_data",
        metadata={
            "num_rows": MetadataValue.int(numrows),
            "expectation_result": MetadataValue.json(expectation_result)
        }
    )
    yield numrows