from dagster import multi_asset, MaterializeResult, AssetSpec, AssetKey, Config
from pydantic import Field
import duckdb
from dagster_duckdb_pandas import DuckDBPandasIOManager


class GenerateTPCHDataConfig(Config):
    scaling_factor: float = Field(default=0.1)


@multi_asset(
    specs=[
        AssetSpec(AssetKey(["tpch", table]), skippable=True)
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
def generate_tpch_data(context, config: GenerateTPCHDataConfig):
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

    # remove landing tables
    conn.execute("drop table IF EXISTS customer")
    conn.execute("drop table IF EXISTS lineitem")
    conn.execute("drop table IF EXISTS nation")
    conn.execute("drop table IF EXISTS orders")
    conn.execute("drop table IF EXISTS part")
    conn.execute("drop table IF EXISTS partsupp")
    conn.execute("drop table IF EXISTS region")
    conn.execute("drop table IF EXISTS supplier")

    # Create schema
    conn.execute(f"CREATE SCHEMA {schema_name}")

    # Generate TPC-H data
    context.log.info(
        f"Generating TPC-H data with scale factor {config.scaling_factor}."
    )
    conn.execute(f"CALL dbgen(sf = {config.scaling_factor})")

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
        yield MaterializeResult(asset_key=AssetKey([schema_name, table_name]))
