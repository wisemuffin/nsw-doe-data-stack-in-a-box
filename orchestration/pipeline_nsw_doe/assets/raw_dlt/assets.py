from typing import Optional

import yaml
from dagster import (
    AssetExecutionContext,
    AutoMaterializePolicy,
    AutoMaterializeRule,
    file_relative_path,
)
from dagster._annotations import public
from dagster_embedded_elt.dlt import (
    DagsterDltResource,
    DagsterDltTranslator,
    dlt_assets,
)
from dlt import pipeline
from dlt.extract.resource import DltResource
from ...dlt_sources.github import github_reactions, github_repo_events


# dlt_configuration_path = file_relative_path(__file__, "../../dlt_sources/dlt_configuration.yaml")
# dlt_configuration = yaml.safe_load(open(dlt_configuration_path))


class GithubDagsterDltTranslator(DagsterDltTranslator):
    @public
    def get_auto_materialize_policy(self, resource: DltResource) -> Optional[AutoMaterializePolicy]:
        return AutoMaterializePolicy.eager().with_rules(
            AutoMaterializeRule.materialize_on_cron("0 0 * * *")
        )


@dlt_assets(
    dlt_source=github_reactions(
        # owner= "wisemuffin",
        # name="nsw-doe-data-stack-in-a-box",
        owner="dagster-io", 
        name="dagster", 
        # access_token = "", #dlt.secrets.value,
        items_per_page=100,
        max_items=10
    )
    .with_resources("issues")
    ,
    dlt_pipeline=pipeline(
        pipeline_name="github_github_reactions",
        dataset_name="raw_github", # schema
        destination="duckdb"
    ),
    name="github",
    # key_prefix=["raw"], # TODO: no prefixing yet
    group_name="raw_github",
    dlt_dagster_translator=GithubDagsterDltTranslator()
)
def github_reactions_dagster_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)



# @dlt_assets(
#     dlt_source=github_repo_events(
#         # owner= "wisemuffin",
#         # name="nsw-doe-data-stack-in-a-box",
#         owner="dagster-io", 
#         name="dagster", 
#         # access_token = "", #dlt.secrets.value,
#         # items_per_page=100,
#         # max_items=10
#     )
#     # .with_resources("repo_events")
#     ,
#     dlt_pipeline=pipeline(
#         pipeline_name="github_repo_events",
#         dataset_name="raw_github", # schema
#         destination="duckdb"
#     ),
#     name="github_evt",
#     # key_prefix=["raw"], # TODO: no prefixing yet
#     group_name="raw_github",
#     dlt_dagster_translator=GithubDagsterDltTranslator()
# )
# def github_repo_events_dagster_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
#     yield from dlt.run(context=context)

