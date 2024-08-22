FROM python:3.10-slim-bullseye

# Checkout and install dagster libraries needed to run the gRPC server
# exposing your repository to dagster-webserver and dagster-daemon, and to load the DagsterInstance

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker \
    pandas  \
    dagster-dbt \
    dagster-docker \
    dbt-fabric \
    dagster-deltalake-pandas \
    dagster-deltalake

RUN apt-get update && apt-get install -y curl gnupg lsb-release
RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
RUN echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/azure-cli.list
RUN apt-get update && apt-get install -y azure-cli

RUN apt-get install sudo -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
RUN sudo apt-get update
RUN sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18


WORKDIR /opt/dagster/app


# Run dagster gRPC server on port 4000

EXPOSE 4001

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
# cant get this to work in docker file, but works in docker-compose
# CMD ["dagster api grpc -h 0.0.0.0 -p 4000 -m demo_pipeline_jaffle_shop"]

# dagster api grpc -h 0.0.0.0 -p 4000 -m demo_pipeline_jaffle_shop

# docker run -it --rm -v /home/dave/.azure-for-docker:/root/.azure \
#     -v /opt/dagster/dagster_home:/tmp/dagster-data \
#     -v /home/dave/data-engineering/cese_dia_analytics/cese_dia_dagster/demo_pipeline_jaffle_shop:/opt/dagster/app/demo_pipeline_jaffle_shop \
#     -v /home/dave/data-engineering/cese_dia_analytics/dbt:/opt/dagster/dbt \
#     demo_pipeline_jaffle_shop bash


# docker run -it --rm -v $HOME/.azure-for-docker:/root/.azure \
#     -v $HOME/data-engineering/cese-dai-analytics/cese_dia_dagster/demo_pipeline_jaffle_shop:/opt/dagster/app/demo_pipeline_jaffle_shop \
#     -v $HOME/data-engineering/cese-dai-analytics/dbt:/opt/dagster/dbt \
#     demo_pipeline_jaffle_shop bash
