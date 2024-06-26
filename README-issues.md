# issues

## Issue - DuckDBPandasIOManager doesnt support drop and create

Currently, the DuckDBPandasIOManager does not support automatically dropping and recreating tables when the schema changes. This limitation is noted in several issues and discussions. Users have requested a feature to allow the IO manager to handle schema changes more gracefully, such as by dropping the table if the schema does not match.

1. Schema Mismatch Handling: When the schema of a table changes (e.g., column names or number of columns), the DuckDBPandasIOManager will fail because it attempts to insert data into an existing table with a mismatched schema.

2. Manual Table Drop: As a workaround, users currently need to manually drop the table in DuckDB before running the asset again to avoid schema mismatch errors.

**Open Issues**: https://github.com/dagster-io/dagster/issues/13098

**Workaround**: using dlt to manage schema evolution. Or if cant use dlt then manually dropping tables.


## Issue - Connection locks on duckdb

Duckdb only allows one connection to have a write connection at a time.

We get around this currently by setting dagster execution to sequential when using duckdb localy.

Would be much better to write in paralel!

**Open Issues**: https://github.com/dagster-io/dagster/issues/18746

## Issue - Dagster empty data frames with data frame to duckdb I/O managers

if an empty dataframe is returned from an asset/op. Impacts DuckDBPandasIOManager.

**Open issues**: https://github.com/dagster-io/dagster/issues/13287

## Issue - dlt google analytics

google analytics full load doesnt work see asset and note on why full load isnt working.

**workaround** as a work around you must delete the logs in duckdb and the logs stored in local state to ensure a full load for google analytics

## Issue - Evidence.dev data refreshing

Warning for Developer: Visuals update when sql in evidence is changed. But source cache doesnt get notified when data changes in database. 🚧 Figure out longer term fix.

# Issues encountered with datansw datasets

## Issue - Data Set - Resource Allocation Model

- Problem masterdataset is a current view of schools, however historic data such as Resource Allocation shows historic school, some of which like 1515, 2037 which are not in current list from datansws master schools
- Each years file the schema changes e.g. naming for original vs estimate... some columns have blanks at start.
- Some files have grand totals at the bottom
