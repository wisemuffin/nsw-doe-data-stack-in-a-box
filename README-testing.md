🚧 currently mirroring gitlab's data team testing below:

### Trusted Data Framework

See the [Trusted Data Framework](/handbook/business-technology/data-team/platform/#tdf) section of our Platform page for a deeper dive into the philosophy behind the Trusted Data Framework.

#### Schema To Golden Data Coverage

We implement 12 categories of Trusted Data Framework (TDF) monitors and tests (monitors are created in and executed by [Monte-Carlo](/handbook/business-technology/data-team/platform/monte-carlo/), tests are created with and executed by dbt):

1. `Freshness monitors` Monitor for unusual delays in table and field updates
1. `Schema monitors` Monitor fields that are added, removed or changed
1. `Volume monitors` Monitor for unusual changes in table size based on the numbers of rows
1. `Field health Monitor` Monitor fields for dips or spikes in stats like % null, % unique, and more. Our ML sets the thresholds.
1. `SQL rule monitor` Write a SQL statement to check for any expressable condition across 1 or more tables in your data.
1. `JSON schema monitor` Monitor for schema changes in JSON data added to a table field.
1. `Dimension tracking` Monitor for changes in the distribution of values within a low-cardinality table field.
1. [Schema tests](/handbook/business-technology/data-team/platform/dbt-guide/#schema-tests) to validate the integrity of a schema
1. [Column Value tests](/handbook/business-technology/data-team/platform/dbt-guide/#column-value-tests) to determine if the data value in a column matches pre-defined thresholds or literals
1. [Rowcount tests](/handbook/business-technology/data-team/platform/dbt-guide/#rowcount-tests) to determine if the number of rows in a table over a pre-defined period of time match pre-defined thresholds or literals
1. [Custom SQL tests](/handbook/business-technology/data-team/platform/dbt-guide/#custom-sql) any valid SQL that doesn't conform to the above categories

Our tests are stored in 2 primary places - either in a YAML file within our [main project](https://gitlab.com/gitlab-data/analytics) or within our [Data Tests](https://gitlab.com/gitlab-data/data-tests) project.

Schema and Column Value tests will usually be in the main project. These will be in `schema.yml` and `sources.yml` files in the same directory as the models they represent.

Rowcount, and any other custom SQL tests will always be in the [Data Tests](https://gitlab.com/gitlab-data/data-tests) project. This is a private project for internal GitLab use only.

##### Tagging

Tagging the tests is an important step in adding new tests. Labeling the test with a [dbt tag](https://docs.getdbt.com/reference/resource-configs/tags/) is how we parse and identify tests when building trusted data dashboards. There are 2 ways to tag tests depending on their type.

The first is by adding tags in the YAML definition. This can be done at the highest level of the YAML definition for source tests, or on the column level for model tests.

```yaml
## Source Labeling in sources.yml
version: 2

sources:
  - name: zuora
    tags: ["tdf","zuora"]

## Model Labeing in schema.yml
version: 2

models:
  - name: zuora_accounting_period_source
    description: Source layer for Zuora Accounting Periods for cleaning and renaming
    columns:
      - name: accounting_period_id
        tags: ["tdf","zuora"]
        tests:
          - not_null
          - unique
```

Each of these examples will apply the tags to all tests nested in the underlying hierarchy.

The second way of adding tags is via the `config` declaration at the top of a test file:

```sql
{{ config({
    "tags": ["tdf","zuora"]
    })
}}

WITH test AS (...)
```

##### General Guidance

- Every model should be tested in a `schema.yml` file
- At minimum, unique fields, not nullable fields, and foreign key constraints should be tested (if applicable)
- The output of dbt test should be pasted into MRs
- Any failing tests should be fixed or explained prior to requesting a review

#### Schema Tests

Schema tests are designed to validate the existence of known tables, columns, and other schema structures. Schema tests help identify planned and accidental schema changes.

All Schema Tests result in a PASS or FAIL status.

##### Schema Test Example

Purpose: This test validates critical tables exist in the Zuora Data Pipeline.

We've implemented schema tests as a [dbt macro](https://docs.getdbt.com/docs/building-a-dbt-project/jinja-macros/). This means that instead of writing SQL, a user can add the test by simply calling the macro. This is controlled by the [`raw_table_existence`](https://dbt.gitlabdata.com/#!/macro/macro.gitlab_snowflake.raw_table_existence) macro.

```sql
-- File: https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/tests/sources/zuora/existence/zuora_raw_source_table_existence.sql
{{ config({
    "tags": ["tdf","zuora"]
    })
}}

{{ raw_table_existence(
    'zuora_stitch',
    ['account', 'subscription', 'rateplancharge']
) }}
```

#### Column Value Tests

Column Value Tests determine if the data value in a column is within a pre-defined threshold or matches a known literal. Column Value Tests are the most common type of TDF test because they have a wide range of applications. Column Value tests are useful in the following scenarios:

- change management: pre-release and post-release testing
- ensuring sums/totals for important historical data meets previously reported results
- ensuring known "approved" data always exists

Column value tests can be added as both YAML and SQL. dbt natively has tests to assert that a column is not null, has unique values, only contains certain values, or that all values in a column are represented in another model (referential integrity).

We also use the [dbt-utils](https://github.com/fishtown-analytics/dbt-utils) package to add even more testing capabilities.

All Column Value Tests result in a PASS or FAIL status.

##### Column Value Test Example 1

Purpose: This test validates the account ID field in Zuora. This field is always 32 characters long and only has numbers and lowercase letters.

Because we use dbt, we have documentation for all of our source tables and most of our downstream modeled data. With in the yaml documentation files, we're able to add tests to individual columns.

```yaml
# File: https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/models/sources/zuora/sources.yml
    - name: account
    description: '{{ doc("zuora_account_source") }}'
    columns:
        - name: id
        description: Primary Key for Accounts
        tags: ["tdf","zuora"]
        tests:
            - dbt_utils.expression_is_true:
                expression: "id REGEXP '[0-9a-z]{32}'"
```

#### Rowcount Tests

The Rowcount test is a specialized type of Column Value test and is broken out because of its importance and utility. Rowcount tests determine if the number of rows in a table over a period of time meet expected pre-defined results. If data volumes change rapidly for legitimate reasons, rowcount tests will need to be updated appropriately.

##### Rowcount Test Example 1

Purpose: This test validates we always had 18,849 Zuora subscription records created in 2019.

This test is implemented as a [dbt macro](https://docs.getdbt.com/docs/building-a-dbt-project/jinja-macros/). This means that instead of writing SQL, a user can add the test by simply calling the macro. This is controlled by the [`source_rowcount`](https://dbt.gitlabdata.com/#!/macro/macro.gitlab_snowflake.source_rowcount) macro.

```sql
-- https://gitlab.com/gitlab-data/data-tests/-/blob/main/tests/sources/zuora/rowcount/zuora_subscription_source_rowcount_2019.sql
{{ config({
    "tags": ["tdf","zuora"]
    })
}}

{{ source_rowcount(
    'zuora',
    'subscription',
    18489,
    "autorenew = 'TRUE' and createddate > '2019-01-01' and createddate < '2020-01-01'"
) }}

```

##### Rowcount Test Example 2

Purpose: We have a fast-growing business and should always have at least 50 and at most 200 new Subscriptions loaded from the previous day. This is controlled by the [`model_new_records_per_day`](https://dbt.gitlabdata.com/#!/macro/macro.gitlab_snowflake.model_new_rows_per_day) macro.

```sql
-- https://gitlab.com/gitlab-data/data-tests/-/blob/main/tests/sources/zuora/rowcount/zuora_subscription_source_model_new_records_per_day.sql
{{ config({
    "tags": ["tdf","zuora"],
    "severity": "warn",
    })
}}

{{ model_new_rows_per_day(
    'zuora_subscription_source',
    'created_date',
    50,
    200,
    "date_trunc('day',created_date) >= '2020-01-01'"
) }}

```

#### Custom SQL

You may have a test in mind that doesn't fit into any of the above categories. You can also write arbitrary SQL as a test. The key point to keep in mind is that the test is *passing* if no rows are returned. If any rows are returned from the query, then the test would fail.

An example of this from the dbt docs:

```sql
{{ config({
    "tags": ["tdf","fct_payments"]
    })
}}

-- Refunds have a negative amount, so the total amount should always be >= 0.
-- Therefore return records where this isn't true to make the test fail
SELECT
    order_id,
    sum(amount) AS total_amount
FROM {{ ref('fct_payments' )}}
GROUP BY 1
HAVING total_amount < 0
```

Any valid SQL can be written here and any dbt models or source tables can be referenced.

#### Merge Request Workflow

🚧