from dagster import asset, Output
import duckdb
from dagster_duckdb_pandas import DuckDBPandasIOManager


@asset(
    name="tpch_data",
    description="Generates TPC-H data using dbgen with scale factor 1",
    io_manager_key="io_manager_dw",
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

    # Verify data generation
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
        yield Output(
            value=None,
            output_name=table,
            metadata={"schema": schema_name, "table": table},
        )
