from dagster import multi_asset, MaterializeResult, AssetSpec
import duckdb
from dagster_duckdb_pandas import DuckDBPandasIOManager


# @asset(
#     name="tpch_data",
#     description="Generates TPC-H data using dbgen with scale factor 1",
#     io_manager_key="io_manager_dw",
# )
@multi_asset(
    specs=[
        AssetSpec(table, skippable=True)
        for table in [
            "customer",
            "lineitem",
            "nation",
            "orders",
            "part",
            "partsupp",
            "region",
            "supplier",
        ]
    ],
    required_resource_keys={"io_manager_dw"},
)
def generate_tpch_data(context):
    # Retrieve the database name from the context
    io_manager_dw: DuckDBPandasIOManager = context.resources.io_manager_dw
    database = io_manager_dw._database
    conn = duckdb.connect(database=database)
    schema_name = "tpch"

    # Check if schema exists and drop it
    schema_exists = conn.execute(
        f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'"
    ).fetchone()
    if schema_exists:
        context.log.info(f"Schema '{schema_name}' exists. Dropping schema and tables.")
        conn.execute(f"DROP SCHEMA {schema_name} CASCADE")

    # Create schema
    conn.execute(f"CREATE SCHEMA {schema_name}")

    # Generate TPC-H data
    context.log.info("Generating TPC-H data with scale factor 1.")
    conn.execute("CALL dbgen(sf = 1)")

    # update the schema
    context.log.info("Updating schema for TPC-H data")
    tables = [
        "customer",
        "lineitem",
        "nation",
        "orders",
        "part",
        "partsupp",
        "region",
        "supplier",
    ]
    for table in tables:
        # would have prefered to `alter table {table} set schema {schema_name}`` but not supported yet see: https://github.com/duckdb/duckdb/discussions/10641
        conn.execute(f"CREATE TABLE {schema_name}.{table} as select * from {table}")

    # Verify data generation
    context.log.info("Verify data generation")
    tables = conn.execute(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'"
    ).fetchall()
    if tables:
        context.log.info(
            f"Generated TPC-H data in schema '{schema_name}' with tables: {', '.join([table[0] for table in tables])}"
        )
    else:
        context.log.error("Failed to generate TPC-H data.")

    for table in tables:
        table_name = table[0]
        yield MaterializeResult(asset_key=table_name)
