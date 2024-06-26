# CESE DIA Analytics 📊

## Todo

🚧working on
deploying to vm
deployment CICD

🐛bugs
- dagster_deltalake supplies a schema for destination table in fabric lakehouse but fabric lakehouse doesnt accept schemas just yet [🐛bug info](https://dev.azure.com/educationtransformation/cese-dai-analytics/_workitems/edit/1)

🔙🪵backlog
- make onboarding easier with Dev containers
- dagster refresh powerbi
- for sources show then with python key in dagster dag
- docs on taskfile
- docs on dbt power users for vscode
- setup linting and formating with black

💩 Not workings
- definitions_example_duckdb.py -- due to no catalog for duckdb wont use
- example onelake_df_ingestion.py -- works but only for one csv file


## Key features

- seperation of business logic and i/o with dagster i/o manager
- speed up data ingestion development with dataframe strait to delta via dagster i/o manager
- standardised and well known transformation framework with dbt's integration with fabric warehouse

## Onboarding 😸

see [dbt-fabric docs](https://learn.microsoft.com/en-us/fabric/data-warehouse/tutorial-setup-dbt) if you get stuck.

### new to dbt?
For more information on dbt:
- Read the [introduction to dbt](https://docs.getdbt.com/docs/introduction).
- Read the [dbt viewpoint](https://docs.getdbt.com/docs/about/viewpoint).
- Join the [dbt community](http://community.getdbt.com/).

### new to fabric
Read this:
- [Fabric docs](https://learn.microsoft.com/en-us/fabric/)
- [T-SQL surface area in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area)
- [Microsoft Fabric: Lakehouse vs Warehouse youtube](https://www.youtube.com/watch?v=34sI2e30JUM)
- [Microsoft Fabric: Lakehouse vs Warehouse ppt](https://publicstoragejs.blob.core.windows.net/presentations/Microsoft%20Fabric%20-%20Lakehouse%20vs%20Warehouse%20-%20James%20Serra.pdf)

## Architecture 🥨

COMING SOON 🚧

transformations with:
- dbt
- pyspark
- sql stored procs
- dataflows gen 2

## Orchistration

COMING SOON 🚧

## Setup Environment 🦞 localy

### setup pre requisite python version

make sure you are on the same version of python (3.10)

```bash
python --version
```

Use pyenv for simpler python version management
```bash
pyenv versions
```

### pre requisite install odbc driver for sql server

[sql server driver install instructions](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows)

e.g. using ubuntu
```bash
$HOME/data-engineering/cese-dai-analytics/dbt/utils/odbc_setup_bash.sh
```

### setup virtual env


```bash
cd ~
mkdir cese_dia_analytics
git pull ...
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### setup dagster
This will setup dagster locally.
Make sure you have [taskfile](https://taskfile.dev/installation/) setup on you env.
```
task dag_setup
```

### get profiles.yml (contains secrets)
Have yet to setup secrets vault. Will just message secerets for now during POC phase.

### .env dagster

TODO: want to make the DAGSTER_HOME dynamic

in ./cese_dia_dagster/cese_dia_dagster is an .env file
change DAGSTER_HOME to your location (has to be absoloute path for local dev)


note if a dagster.yml file exists in DAGSTER_HOME location then dagster will use that for instance config.

### install azure cli

see [Azure CLI instructions](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

then login

```bash
az login
```



### setup dbt connection to fabric data warehouse

Create a dbt `profiles.yml` with the following:

```yml
config:
  partial_parse: true
jaffle_shop:
  target: fabric-dev
  outputs:    
    fabric-dev:
      authentication: CLI
      database: <put the database name here>
      driver: ODBC Driver 18 for SQL Server
      host: <enter your sql endpoint here>
      schema: dbt_<your name like dgriffiths> # you can work in your own schema when developing a feature
      threads: 4
      type: fabric
```

This file configures the connection to your warehouse in Microsoft Fabric using the dbt-fabric adapter.

### load all dbt packages

```bash
dbt deps
```


### validate your connection

```bash
dbt debug
```

if this returns All checks passed then you are good to go 🎉

### vscode extentions (optional)

- [dbt pwoer users](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user)

## documentation 📃

Generate documentation for the project:
```bash
$ dbt docs generate
```

View the documentation for the project:
```bash
$ dbt docs serve
```


# Debugging Dagster


## debuging end to end with dagit UI
simply run the dagit ui in debug mode in vscode via .vscode/launch.json:

```json
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Dagster: Debug Dagit UI",
        "type": "python",
        "request": "launch",
        "module": "dagster",
        "justMyCode": false,
        "args": ["dev",
                    "-f",
                    "${workspaceFolder}/cese_dia_dagster/cese_dia_dagster/definitions_example_delta_azure.py"
            ],
        "envFile": "${workspaceFolder}/.env"
      }
    ]
  }
```

## local debuging without the UI

This way we skip spinning up the dagster UI saving time when developing. But we still want to test with the dagit UI before deployment.

You just need to change which assets you want run in `./debug`

debug mode in vscode via .vscode/launch.json:

```json
{
    "version": "0.2.0",
    "configurations": [
    {
      "name": "Dagster: debug with .debug.py",
      "type": "python",
      "request": "launch",
      "cwd": "${workspaceFolder}/cese_dia_dagster",
      "module": "debug",
      "justMyCode": false,
      "envFile": "${workspaceFolder}/.env",
    },
}
```

# Deployment

## Docker

[source](https://ibrahimhkoyuncu.medium.com/dagster-complete-guide-to-deploy-multiple-data-pipelines-to-dagster-on-docker-environment-aae47028a4ce)

In this Dockerfile, just upload your data pipeline to relevant working directory and start dagster api with gRPC connection. If you realize that, port number is same with workspace.yaml which points to this code location. If you have multiple code locations(data pipelines) you should create an docker image for each pipeline with different gRPC port and then add them to workspace.yml file and docker-compose file. To create an docker image for this pipeline run below command.
```bash
docker build -t demo_pipeline_jaffle_shop $HOME/data-engineering/cese-dai-analytics/cese_dia_dagster/demo_pipeline_jaffle_shop
```

```bash
docker build -t demo_pipeline_y $HOME/data-engineering/cese-dai-analytics/cese_dia_dagster/demo_pipeline_y
```

Both dagster-webserver and dagster-daemon services will use same image which is created from Dockerfile. Be aware that we copy our configurations files which are dagster.yml and workspace.yml into this image. So dagster-daemon services can read workspace.yml and trigger pipeline’s jobs according to it.

```bash
cd ..
docker build -t dagster $HOME/data-engineering/cese-dai-analytics/cese_dia_dagster/
```

### Azure CLI doesnt work in docker any more :(
[Workarounds](https://endjin.com/blog/2022/09/using-azcli-authentication-within-local-containers)


### fixing azure cli

cd /mnt/c/users/<your-username>
mkdir $HOME/.azure-for-docker
AZURE_CONFIG_DIR=$HOME/.azure-for-docker az login --use-device-code


### setup dbt connection to fabric data warehouse

Create a dbt `profiles.yml` with the following:



### docker compose up
```bash
$HOME/data-engineering/cese-dai-analytics/cese_dia_dagster
docker compose up
```

### testing cicd
make code changes
pull latest changes
```bash
git pull
cd $HOME/data-engineering/cese-dai-analytics/cese_dia_dagster
docker compose up -d --no-deps --build demo_pipeline_jaffle_shop
```

- works for dagster but not dbt, maybe need to parse always before?

# updating dagster

```bash
 pip install dagster==1.6.0 dagster-webserver==1.6.0 dagster-dbt==0.22.0 dagster-duckdb==0.22.0 dagster-duckdb-pyspark==0.22.0 dagster-duckdb-pandas==0.22.0 dagster-deltalake-pandas==0.22.0 dagster-aws==0.22.0
 ```
