
{% docs dbt_audit %}
Used to append audit columns to a model.

This model assumes that the final statement in your model is a `SELECT *` from a CTE. The final SQL will still be a `SELECT *` just with 6 additional columns added to it. Further SQL DML can be added after the macro call, such as ORDER BY and GROUP BY.

There are two internally calculated date values based on when the table is created and, for an incremental model, when data was inserted.

```sql
WITH my_cte AS (...)
{% raw %}
{{ dbt_audit(
    cte_ref="my_cte", 
    created_by="@gitlab_user1", 
    updated_by="@gitlab_user2", 
    created_date="2019-02-12", 
    updated_date="2020-08-20"
) }}
{% endraw %}
ORDER BY updated_at
```

{% enddocs %}


{% docs get_keyed_nulls %}

This macro generates a key for facts with missing dimensions so when the fact table is joined to the dimension it joins to a record that says it's unknown as in

```sql
SELECT * 
FROM DIM_GEO_AREA 
WHERE DIM_GEO_AREA_ID = MD5(-1);
```

which has:

```
***************************[ 1 ]***************************
DIM_GEO_AREA_ID    | 6bb61e3b7bce0931da574d19d1d82c88
GEO_AREA_NAME      | Missing geo_area_name
```

Generally this should be used when creating and keying on new dimensions that might not be fully representing in the referencing tables
{% enddocs %}


{% docs scd_latest_state %}
This macro pick up the latest state when data is ingested as SCD type. For this purpose, to ensure we load only the latest state of data, will use `_task_instance` column as a criteria (this can be redefined). Currently we do a `max` on the defined `_task_instance` column, so its important to take a proper column to select.
Example, if we have data records in the `RAW` layer like:

| ID | DATE |
| ---- | ---- |
|1| `2022-01-01`|
|1| `2022-02-02`|
|1| `2022-03-28`|

using this macro (and treating `DATE` ask the `_task_instance`) should reflect and show in the `PREP` layer as:

| ID | DATE |
| ---- | ---- |
|1| `2022-03-28`|

as this record is the recent one. We need this approach for some specific use case.

{% enddocs %}

{% docs scd_type_2 %}
This macro inserts SQL statements that turn the inputted CTE into a [type 2 slowly changing dimension model](https://en.wikipedia.org/wiki/Slowly_changing_dimension#Type_2:_add_new_row). According to [Orcale](https://www.oracle.com/webfolder/technetwork/tutorials/obe/db/10g/r2/owb/owb10gr2_gs/owb/lesson3/slowlychangingdimensions.htm), "a Type 2 SCD retains the full history of values. When the value of a chosen attribute changes, the current record is closed. A new record is created with the changed data values and this new record becomes the current record. Each record contains the effective time and expiration time to identify the time period between which the record was active."

In particular, this macro adds 3 columns: `valid_from`, `valid_to`, and `is_currently_valid`. It does not alter or drop any of the existing columns in the input CTE.
* `valid_from` will never be null
* `valid_to` can be NULL for up to one row per ID. It is possible for an ID to have 0 currently active rows (implies a "Hard Delete" on the source db)
* `is_currently_active` will be TRUE in cases where `valid_to` is NULL (for either 0 or 1 rows per ID)

The parameters are as follows:
  * **primary_key_renamed**: The primary key column from the `casted_cte`. According to our style guide, we usually rename primary keys to include the table name ("merge_request_id")
  * **primary_key_raw**: The same column as above, but references the column name from when it was in the RAW schema (usually "id")
  * **source_cte**: (defaults to '`distinct_source`). This is the name of the CTE with all of the unique rows from the raw source table. This will always be `distinct_source` if using the `distinct_source` macro.
  * **casted_cte**: (defaults to `renamed`). This is the name of the CTE where all of the columns have been casted and renamed. Our internal convention is to call this `renamed`. This CTE needs to have a column called `valid_from`.

This macro does **not** reference anything specific to the pgp data sources, but was built with them in mind. It is unlikely that this macro will be useful to anything outside of pgp data sources as it was built for a fairly specific problem. We would have just used dbt snapshots here except for the fact that they currently don't support hard deletes. dbt snapshots should be satisfactory for most other use cases.

This macro was built to be used in conjunction with the distinct_source macro.

{% enddocs %}



{% docs simple_cte %}
Used to simplify CTE imports in a model.

A large portion of import statements in a SQL model are simple `SELECT * FROM table`. Writing pure SQL is verbose and this macro aims to simplify the imports.

The macro accepts once argument which is a list of tuples where each tuple has the alias name and the table reference.

Below is an example and the expected output:

```sql
{% raw %}
{{ simple_cte([
    ('map_merged_crm_account','map_merged_crm_account'),
    ('zuora_account','zuora_account_source'),
    ('zuora_contact','zuora_contact_source')
]) }}

, excluded_accounts AS (

    SELECT DISTINCT
      account_id
    FROM {{ref('zuora_excluded_accounts')}}

)
{% endraw %}
```

```sql
WITH map_merged_crm_account AS (

    SELECT * 
    FROM "PROD".common.map_merged_crm_account

), zuora_account AS (

    SELECT * 
    FROM "PREP".zuora.zuora_account_source

), zuora_contact AS (

    SELECT * 
    FROM "PREP".zuora.zuora_contact_source

)

, excluded_accounts AS (

    SELECT DISTINCT
      account_id
    FROM "PROD".legacy.zuora_excluded_accounts

)
```

{% enddocs %}
