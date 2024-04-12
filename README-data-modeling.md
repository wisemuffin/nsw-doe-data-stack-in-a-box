# Data Modelling
## Model Structure
Kimball-style warehouse

### Sources

naming: `raw__<source>__<source table name>`

All raw data will still be in the RAW database. These raw tables are referred to as source tables or raw tables. They are typically stored in a schema that indicates its original data source, e.g. datahub


### Staging

naming: `stg__<source>__<source table name>`

We are enforcing a very thin staging layer on top of all raw data. This directory is where the majority of source-specific transformations will be stored. These are “staging” models that pull directly from the raw data and should **do only** the following:

- Rename fields to user-friendly names
- Cast columns to appropriate types
- Minimal transformations that are 100% guaranteed to be useful for the foreseeable future. An example of this is parsing out the Salesforce ID from a field known to have messy data.

The following should **not** be done in a staging model:

- Removing data
- Transformations that fundamentally alter the meaning of a column

Even in cases where the underlying raw data is perfectly cast and named, there should still exist a source model which enforces the formatting. This is for the convenience of end users so they only have one place to look and it makes permissioning cleaner in situations where this perfect data is sensitive.




### Integration

naming: `int__<entity_name>`

As soon as you get multiple sources feeding into one entity you need an integration model. For example if you have two CRMs (Salesforce, and Hubspot) that both have the entity deal, then you need to create a deal integration model.

If you know a entity will have multiple source in the future its best to build the integration layer from the get go to reduce future re factoring.

should **do only** the following:

The following should **not** be done in a integration model:

- Removing data
- Transformations that fundamentally alter the meaning of a column

### dimensional

naming: `fct__<name>` or `dim__<name>`

This directory is where the majority of business-specific transformations will be stored. This layer of modeling is considerably more complex than creating source models, and the models are highly tailored to the analytical needs of business. This includes:

- Filtering irrelevant records
- Choosing columns required for analytics
- Renaming columns to represent abstract business concepts
- Joining to other tables
- Executing business logic
- Modelling of fct_and dim_ tables following Kimball methodology

### saved queries

naming: 'svd__<analytics use case>'

Saved queries are a way to save commonly used queries in MetricFlow. You can group metrics, dimensions, and filters that are logically related into a saved query.

🚧 TODO


### Sensitive Data

All the data is publiclly avaialbe so no sensitive data exists in this project.

However, we can simulate what we do with sensative data in the following ways.

🚧 TODO


### General

- Model names should be as obvious as possible and should use full words where possible, e.g. `accounts` instead of `accts`.

- Documenting and testing new data models is a part of the process of creating them. A new dbt model is not complete without tests and documentation.


- All `{{ ref('...') }}` statements should be placed in CTEs at the top of the file. (Think of these as import statements.)
    - This does not imply all CTE's that have a `{{ ref('...') }}` should be `SELECT *` only. It is ok to do additional manipulations in a CTE with a `ref` if it makes sense for the model

- If you want to separate out some complex SQL into a separate model, you absolutely should to keep things DRY and easier to understand. The config setting `materialized='ephemeral'` is one option which essentially treats the model like a CTE.
