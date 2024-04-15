<!-- ![NSW Department of Education logo](.github/static/nsw-doe.png) -->

<img src=".github/static/nsw-doe.png" width="150" >

# Welcome to New South Wales Department of Education (NSW DOE) data stack in a box

🚧 ![CI Checks](https://github.com/gwenwindflower/octocatalog/actions/workflows/ci.yml/badge.svg) 

This is an data-stack-in-a-box based data from [NSW Education Data Hub](https://data.cese.nsw.gov.au/). With the push of one button you can have your own data stack!

> [!IMPORTANT]  
> Click below 👇🏼 to setup your own free data stack packed with [NSW Department of Education](https://education.nsw.gov.au/) data.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/wisemuffin/nsw-doe-data-stack-in-a-box?quickstart=1)

## Objectives
[NSW Department of Education](https://education.nsw.gov.au/) data stack in a box has two objectives:
1)	Getting humans excited about the data within the NSW Department of Education.
2)	Level up our data stack by demoing features in the data stack that we are lacking or need to improve in [NSW Department of Education](https://education.nsw.gov.au/). These demos will start the conversation on what features we want to prioritise.

## Principals
Simple one button click, that sets you up with your own blazingly fast data stack
`completely free` 💲💲💲. 

## Audience
The project is designed to be very simple but allow you the flexibility for you to go as deep you like!
- **I want to analyse and gain insights into the data.** With the infrastructure free and deployed in one click you don’t need to worry about any implementation details. You can skip straight to analysing and training models on top of your own local warehouse.
- **Interested in modelling via SQL?** We got you covered with a environment setup for DBT.
- **Love DevOps and platform engineering?** Check out our Orchestration, CICD pipelines, and automation such as linting, data diffs ect.



## Overview of Project (Architecture) 🥨


![Data Architecture](.github/static/architecture.png)


> ![Info] We are simply going to extract data from the [NSW Education Data Hub](https://data.cese.nsw.gov.au/) and load it into our in memory data warehouse 🦆, model, clean, and analyse our data.


> [!WARNING]  
> The datasets from ACARA and NSW DOE are based on static urls. These URLs will break 💣 in the future. I will try to keep an eye out for this every few months. 🚧 TODO setup discussion on limitations with public datasets.


<!-- ## Option tooling (Architecture) 🥨

> ![Info] These components are purley for demoing purposes. They are not needed in the project.

- Tableau
  - ai monitoring
- Power BI
- Open Metadata
- DBT Cloud 
  - semantic layer
  - column level linage
-->




## Bus Matrix

| Fact          | Status | Dim School                            | Dim Schoolastic Year| Dim Calendar Year | Fact Source Url | Notes|
| ------------- | ---------------- | -------------------------------------- | --- | --- | ---| ---|
| `Full-time equivalent (FTE) enrolments` | ❌ | ✅ | ✅ | ❌ | https://data.cese.nsw.gov.au/data/dataset/resource-allocation-model | Not doing. No temporal data. |
| `Resource Allocation Model (RAM)`  | 🚧 | ✅  | ❌ | ✅ | https://data.cese.nsw.gov.au/data/dataset/resource-allocation-model| Each file name is differnt and path is also different will need to manually check and update path |
|`Specialist support classes` | ❌ | ✅  | ❌ | ❌ |https://data.cese.nsw.gov.au/data/dataset/specialist-support-classes-by-school-and-support-needs-type | Not doing. No temporal data.
|`Attendance rates` | ❌ `cancelled` | ✅  | ❌ | ✅ | https://data.cese.nsw.gov.au/data/dataset/student-attendance-rate-by-schoo | Dont have numerator and denominator so cant aggregate this fact table |
|`Multi age or composite classes` | 🚧 | ✅  | ❌ | ✅ | https://data.cese.nsw.gov.au/data/dataset/multi-age-or-composite-classes-in-nsw-government-schools | Required some pivoting |
|`Staff` | 🚧 | ❌ | ❌ | ✅ | https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia/staff-numbers||
|`Students` | 🚧 | ❌ | ❌ | ✅ | https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia/student-numbers||

## ERD

[Dimensional ERD check out](./ERD.md)

## Give me more data!

### Data that I want from DOE

- `Number of techers per school` was on the data hub but was removed citing will now be reported by ABS. But ABS data isnt at a school level.

### Data from ACARA / NESA

- `NAPLAN` and `HSC attainment` by school. Can get NAPLAN by school going to ACARA's [MySchool](https://www.myschool.edu.au/school/41307) but no easy way to get a view for all schools data.



## Key features

- seperation of business logic and i/o with dagster i/o manager
- co pilot

**Accelerate data modeling Development**

- exploritory data analysis whilst you data model! build models, test, visualise iterate in vscode ![dbt-power-users](.github/static/dbt-power-users-test-and-vis-queries.gif)
- Navigate data models with model level lineage ![Naviate data models](.github/static/dbt-power-users-quick-navigation.gif)
- [Defer to prod](https://docs.myaltimate.com/test/defertoprod/) - dont copy accross all of the prod models into dev when you can simply reference them.

[Full list of dbt accelerations from dbt power users](https://docs.myaltimate.com/)

📓 some additional features below that use AI features require a API key from [Accelerate](https://www.altimate.ai/) but in this project just using the open source free version:

<!-- > [!NOTE]  
> some additional features below that use AI features require a API key from [Accelerate](https://www.altimate.ai/) but in this project just using the open source free version: -->

| :memo:        | some additional features below that use AI features require a API key from [Accelerate](https://www.altimate.ai/) but in this project just using the open source free version:       |
|---------------|:---------------------------------------------|


- Document data models with AI ![AI docs](.github/static/dbt-altimate-ai-documentation.gif)
- Explore column level lineage and carry out impact analysis![lineage and impact analysis](.github/static/dbt-power-users-lineage-and-impact-analysis-column-lineage.gif)


**Accelerate data data ingestion**

Just create a python pandas dataframe and put that logic into the orchistrator dagster

> [!WARNING]  
> Pandas will only scale so far. But for +95% of the work we do at NSW DOE analytics its probably enough.


Data Wrangler
Exploritory analysis
cleaning - string from example 
Dont need to memorise Pandas API. Drag and dops converts to Pandas 🐼

![Data Wangler](.github/static/data-wrangler.gif)


**testing**

dagster asset checks
dbt tests
piplines should master metadata including tests...

🚧 anomily detection
🚧 schema validation
🚧 dbt unit tests

**debugging**

🚧 debuggin demo


**data consumers**

🚧 data vis
🚧 data science


**CICD**
🚧 branch deployments
🚧 linting, sql fluff ect
🚧 data quality test

## Key Features - where we dont have a good open source option

**semantic/metrics layer**

🚧 have a hack to use part of dbt's semantic layer. The hack is very limited but at least I can use dbt semantic layer locally and for testing even if its missing the enterprise features.

**AI metrics**

🚧 AI metrics e.g. tableau


## Todo

### 🚧working on
- DOE data
  - 🚧 facts and dims
- check out scd_latest_state and scd_type 2 macros from gitlab
- pandera
- use snapshots?
- tests
  - ✅ relationship tests from fact to dims
  - For dimensions, we can test for the existence of the MD5('-1') (missing) dimension_id, and total row counts.
  - For facts, we can test to ensure the number of records/rows is not expanded due to incorrect granularity joins.
- evidence
  - error when evidence and etl going at same time: `IO Error: Could not set lock on file "/home/dave/data-engineering/nsw-doe-data-stack-in-a-box/reports/sources/nsw_doe_data_stack_in_a_box__dev/nsw_doe_data_stack_in_a_box__dev.duckdb": Conflicting lock is held in /home/dave/.config/nvm/versions/node/v20.11.1/bin/node (PID 1516344). However, you would be able to open this database in read-only mode, e.g. by using the -readonly parameter in the CLI. See also https://duckdb.org/docs/connect/concurrency` 
    - Evidence connection to duckdb doesnt close. Have to wait for this to be fixed via this [issue](https://github.com/evidence-dev/evidence/issues/1060)
    - Temp work around is to connect tell engineers to stop the evidence proccess? or could force this with a task?



### 🧱 Blocked
- using jupyter notebooks as upstream data transformations in dagster as assets (all good if they are the last part of the dag). Keen an eye on this [thread](https://github.com/dagster-io/dagster/issues/10557). Also note its possible to do with Ops just not Assets yet for example `AssetsDefinition.from_op(my_asset_name)`
- asset checks - anomily detection 🌿 feature/asset-checks
  - working on anomily detection. asset check in defintion file not supported yet in dagster
  - 🧱 dagster version currently 1.6.11 but i need 1.6.13 for asset checks i think
- dbt metrics via semantic layer using dbt cloud. 🧱 will need mother duck to accept v 0.10
- dbt power user lineage no metrics and saved queries. Currently can only do this in dbt cloud.
- motherduck not supported in dbt cloud yet.
- dbt saved queries node is causing issues with dagster 🚧 TODO
- dagster data quality - quarantine if fail asset checks. Currently no examples for this type of workflow.
- dagster data quality - asset checks for partitions not supported yet
- sql tools for duckdb locks database [issue](https://github.com/evidence-dev/sqltools-duckdb-driver/issues/5).

### 🔙🪵backlog
- change all gif to be NSW based
- python package manager uv is so much faster but cant use in taskfile. Explore this some more
  - speed up codespace by using uv as a python package manager
- Motherduck upgrade to 0.10.X eta end of march
  - waiting on motherduck to 0.10.0 to get sql tools to work & backwards compatability of duckdb versions
  - backwards compatability
- dbt unit tests (in preview in dbt core 1.8) want to add these soon but dont want to use 1.8 yet until duckdb and mother duck have been updated.
- limitation, when dbt model fails all downstream fails (i.e. if have depency on any other dbt table). To investigate.
- deployment CICD
  - generate docs on merge for ERDs
  - check metricflow config see `task mf_check`
  - dbt data tests
  - dbt unit tests
  - dbt data freshness
  - data diffs
  - sqlfluff
  - that python rust package for python linting ect
- devcontainer load optimisation, could remove ipywidgets and pandas profiling
- docs on taskfile
- sqlfluff
- setup linting and formating with black - user Ruff
- setup discussion on limitations with public datasets.
- sensitive data demo [example](https://handbook.gitlab.com/handbook/business-technology/data-team/platform/dbt-guide/#sensitive-data)
- demo [gdpr delete dbt macro](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/macros/warehouse/gdpr_delete.sql)
- integrated the mermaid diagram output with dbt docs and served it with repo pages


💩 Limitations / hard to do 😢😭
- dont have a great way to check schema of incoming data. e.g. dlthub would be a geat framework to use for this. Can use Pandera
- dynamic data masking policies in duckdb/motherduck?
- auto start dagster in codespace and popup webserver but also want evidence-dev to also pop up?
  - "postStartCommand": "task dag" does this mean the codesandbox wont closed down?
  - "postStartCommand": evidence steps dont run due to dagit runs continiously
  - for now will just click on forwarded ports
- dynamic check for dbt's manifest.json not working. For now will always parse dbt project.
- duckdb locks from different processes. Think this is solved in duckdb 0.10.0?
- pandas to duckdb io manager (see notes in jaffle shop raw_orders_py when recieves empty df then it wont use the dtypes from dataframe when building db objects. i.e. strings are getting convereted to int32...
- great expecations 🌿 feature/great-expectations
  - i really want to test with GE and use the quarantine pattern for data like in: https://youtu.be/wAayC-J9TsU?si=MYx_eG3ZOB_q_LDS
  - dagster isnt maintaining dagster_ge [🔗 link](https://github.com/dagster-io/dagster/blob/1.6.13/examples/with_great_expectations/README.md)
  - dagster seems to be more focused on asset checks. But i want to also handle quarantine data
  - some issues with dagster and GE to solve
    - need to remove dbt-metricflow[duckdb] to get great expecations to work for now. **Error** because you require dbt-metricflow[duckdb] and you require great-expectations>=0.17.0, we can conclude that the requirements are unsatisfiable.
    - need to setup dagster test suite

### Done
- [DBT ERDs](https://github.com/datnguye/dbterd), The Mermaid integration is the best of all IMO and can be automated for diagram generation.
  - ✅ duckdb doesnt support merge so missing_member_column is failing (hook in dim__school)
  - ✅ TODO relationship tests allow multiple to go to ....
  - ✅ need to figure out how to use python to programtically only get _sk columns and x columns. Then where to save?
- ✅ dbt power users cant build or test models yet due to path issues
- ✅ architecture diagram use https://excalidraw.com/
- ✅ metric flow can store metric results in csv then load then back into duckdb each day with `mf query --metrics orders --csv ./dave.csv` not ideal but dbt doesnt expose serice layer or APIs. Workaround is Create and run Exports to save metrics queries as tables in your data platform via the CSV generated above.
  - first un comment the saved query then run `mf query --saved-query new_customer_orders --csv ./dave-saved-query.csv`. saved query currently not working with dagster.
  - need to then load into duckdb. Could use CLI then take file, load into dataframe then load into duckdb.
- ✅ machine learning - e.g. facebook prophecy
- ✅ failing partitions when nothing returned by df
- ✅ dagster auto start container
- ✅ duckdb_pandas_io_manager is legacy and should be replaced by  DuckDBPandasIOManager but currently getting duckdb locks so trying to figure out what caused this
- ✅ example metrics layer - saved queries vs exports

## Learnings 🚧
- dbt merge duckdb - duckdb doesnt have merge. The default [get_merge_sql](https://github.com/dbt-labs/dbt-core/blob/7eb6cdbbfbb239f1d9af24d256df228733a4c2df/core/dbt/include/global_project/macros/materializations/models/incremental/merge.sql#L35-L50) wont work for duckdb. dbt-duckdb doesnt have a `duckdb__get_merge_sql`.
  - work around for now macro `duckdb__get_delete_insert_merge_sql` in dbt-duckdb.
- dbt-core macros are stored in `.venv/lib/<py version>/site-pacakages/dbt/global_project/macros`
  - i found this out after understanding `.venv/lib/<py version>/site-pacakages/dbt_core-1.7.9.dist-info/RECORD` contains where python code was added
- dbt hooks - post- and pre-hook dont show up in CLI. Need to check log file. They also arnt referenced as hooks. So need to search after model for additional sql run after
- [dbterd](https://dbterd.datnguyen.de) which turns your [dbt relationship data quality checks](https://docs.getdbt.com/docs/build/tests#generic-data-tests) into an ERD.
  -- option 1 - write as a mermaid file and keep in git repo
  -- option 2 - then serve your docs with [dbdocs](https://dbdocs.io/) this uses the popular open-source database markup language DBML example option 2:
  -- can use python script `ERD_generation.py` or CLI
  ```bash
    dbt docs generate
    dbterd run -s "wildcard:*fct_*" -s "wildcard:*dim_*" --target mermaid --artifacts-dir "./target" --output "./target" --output-file-name "output.md" --omit-columns
    echo \`\`\`mermaid > ./target/ERD.md
    echo --- >> ./target/ERD.md
    echo title: Sample ERD >> ./target/ERD.md
    echo --- >> ./target/ERD.md
    cat ./target/output.md >> ./target/ERD.md
    echo \`\`\` >> ./target/ERD.md
  ```
- dbt power users vscode extension missing [auto completion for columns issue](https://github.com/AltimateAI/vscode-dbt-power-user/issues/79)
- Use [Scaffold tables](https://handbook.gitlab.com/handbook/business-technology/data-team/platform/edw/#common-mart) are useful when tools like Tableau which may necessitate a full dataset for relationships  
  - [scaffold example sql](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/models/common_mart_sales/reports/rpt_scaffold_sales_funnel.sql) 
- can use mermaid diagrams in markdown for github and gitlab
- dynamic data masking possible in warehouse using tags (see snowflake dynamic data masking)
- microsoft clipchap and my phone works really well. Also integrates with sniping tool
- python venvs bin and lib folders. bin has executables e.g. cli. With dbt_metricflow we can run `python -m dbt_metricflow.cli.main list metrics` or `python -m dbt.cli.main --help` as the main.py has a `if __name__ = '__main':`
  - this allows us to run our executables as either python modules for debuging. For CICD just install the CLI.
- uv python currently doesnt seem to have the correct python location when activating the venv for the first time. I had to deactive then re activate again to solve it.
- dagster dbt doesnt like saved queries. As a work around have to remove via selection e.g. '@dbt_assets(..., exclude="*saved_query")'
- dagster assets can set deps instead of loading in a asset via io to make a dependancy

## Issues encountered with Datahub datasets

### Data Set - Resource Allocation Model
- Problem masterdataset is a current view of schools, however historic data such as Resource Allocation shows historic school, some of which like 1515, 2037 which are not in current list from datahubs master schools
- Each years file the schema changes e.g. naming for original vs estimate... some columns have blanks at start.
- Some files have grand totals at the bottom

## Disclaimer

Due to the evolving nature of school information and local enrolment areas, no responsibility can be taken by the NSW Department of Education, or any of its associated departments, if information is relied upon. For example, but not limited to, real estate purchases or rentals where the school intake zone data is used as a reference source.

## Contributing

### Contributing - Data Analyses & Science

🚧 TODO

### Contributing - Data Modeling

I have been following the gitlab's data team's handbook for modeling, naming convetions and testing. 

I am pretty relaxed with standards in this project. But please read through these before developing to help standise the modeling:

- [Enterprise data warehouse](https://handbook.gitlab.com/handbook/business-technology/data-team/platform/edw/)
- Tests
- SQL style guide


Differences to gitlab's data team's handbook:

1) Raw and other schema's 🚧 TODO - simplify CICD have just used one schema, prefix should be enough
2) staging layer added between raw and prep layers.


#### Contributing - Data Modeling - Checklist

- Read through the standards above.
- update ERDs. [dbterd](https://dbterd.datnguyen.de) which turns your [dbt relationship data quality checks](https://docs.getdbt.com/docs/build/tests#generic-data-tests) into an ERD.

```bash
dbt docs generate
.venv/bin/python ERD_generation.py
```