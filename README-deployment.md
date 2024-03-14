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


