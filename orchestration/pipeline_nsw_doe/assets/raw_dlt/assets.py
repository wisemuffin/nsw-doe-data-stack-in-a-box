import os
from typing import Optional

from dagster import (
    AssetExecutionContext,
    AssetKey,
    AutoMaterializePolicy,
    AutoMaterializeRule,
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
from ...dlt_sources.google_analytics import google_analytics
from ...dlt_sources.nsw_doe import nsw_doe_enrolments

# dlt_configuration_path = file_relative_path(__file__, "../../dlt_sources/dlt_configuration.yaml")
# dlt_configuration = yaml.safe_load(open(dlt_configuration_path))

NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA: str = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA", "schema_not_set"
)


class GithubDagsterDltTranslator(DagsterDltTranslator):
    @public
    def get_auto_materialize_policy(
        self, resource: DltResource
    ) -> Optional[AutoMaterializePolicy]:
        return AutoMaterializePolicy.eager().with_rules(
            AutoMaterializeRule.materialize_on_cron("0 0 * * *")
        )

    @public
    def get_asset_key(self, resource: DltResource) -> AssetKey:
        """Defines asset key for a given dlt resource key and dataset name.

        Args:
            resource (DltResource): dlt resource / transformer

        Returns:
            AssetKey of Dagster asset derived from dlt resource

        """
        return AssetKey(f"{resource.name}")

    @public
    def get_deps_asset_keys(self, resource: DltResource):  # -> Iterable[AssetKey]:
        """Defines upstream asset dependencies given a dlt resource.

        Defaults to a concatenation of `resource.source_name` and `resource.name`.

        Args:
            resource (DltResource): dlt resource / transformer

        Returns:
            # Iterable[AssetKey]: The Dagster asset keys upstream of `dlt_resource_key`.
            have set this to none, as DLT is usually the source, and dont want to complicate graph

        """
        # return [AssetKey(f"{resource.source_name}")] #[AssetKey(f"{resource.source_name}_{resource.name}")]


@dlt_assets(
    dlt_source=github_reactions(
        owner="wisemuffin",
        name="nsw-doe-data-stack-in-a-box",
        # owner="dagster-io",
        # name="dagster",
        # access_token = "", #dlt.secrets.value,
        items_per_page=100,
        max_items=10,
    ),
    # .with_resources("issues")
    dlt_pipeline=pipeline(
        pipeline_name="github_github_reactions",
        dataset_name=NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,  # schema
        destination="duckdb"
        if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev") == "dev"
        else "motherduck",
    ),
    name="github",
    # key_prefix=["raw"], # TODO: no prefixing yet
    group_name="raw_github",
    dlt_dagster_translator=GithubDagsterDltTranslator(),
)
def github_reactions_dagster_assets(
    context: AssetExecutionContext, dlt: DagsterDltResource
):
    yield from dlt.run(context=context)


@dlt_assets(
    dlt_source=github_repo_events(
        owner="wisemuffin",
        name="nsw-doe-data-stack-in-a-box",
        # owner="dagster-io",
        # name="dagster",
        # access_token = "", #dlt.secrets.value,
        # items_per_page=100,
        # max_items=10
    ),
    # .with_resources("repo_events")
    dlt_pipeline=pipeline(
        pipeline_name="github_repo_events",
        dataset_name=NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,  # schema
        destination="duckdb"
        if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev") == "dev"
        else "motherduck",
    ),
    name="github_evt",
    # key_prefix=["raw"], # TODO: no prefixing yet
    group_name="raw_github",
    dlt_dagster_translator=GithubDagsterDltTranslator(),
)
def github_repo_events_dagster_assets(
    context: AssetExecutionContext, dlt: DagsterDltResource
):
    yield from dlt.run(context=context)


class GoogleAnalyticsDagsterDltTranslator(DagsterDltTranslator):
    @public
    def get_auto_materialize_policy(
        self, resource: DltResource
    ) -> Optional[AutoMaterializePolicy]:
        return AutoMaterializePolicy.eager().with_rules(
            AutoMaterializeRule.materialize_on_cron("0 0 * * *")
        )

    @public
    def get_asset_key(self, resource: DltResource) -> AssetKey:
        """Defines asset key for a given dlt resource key and dataset name.

        Args:
            resource (DltResource): dlt resource / transformer

        Returns:
            AssetKey of Dagster asset derived from dlt resource

        """
        return AssetKey(f"{resource.name}")

    @public
    def get_deps_asset_keys(self, resource: DltResource):  # -> Iterable[AssetKey]:
        """Defines upstream asset dependencies given a dlt resource.

        Defaults to a concatenation of `resource.source_name` and `resource.name`.

        Args:
            resource (DltResource): dlt resource / transformer

        Returns:
            # Iterable[AssetKey]: The Dagster asset keys upstream of `dlt_resource_key`.
            have set this to none, as DLT is usually the source, and dont want to complicate graph

        """
        # return [AssetKey(f"{resource.source_name}")] #[AssetKey(f"{resource.source_name}_{resource.name}")]


GA_QUERIES = [
    {
        "resource_name": "raw_google_analytics_sample_analytics_data1",
        "dimensions": ["browser", "city"],
        "metrics": ["totalUsers", "transactions"],
    },
    {
        "resource_name": "raw_google_analytics_sample_analytics_data2",
        "dimensions": ["browser", "city", "dateHour"],
        "metrics": ["totalUsers"],
    },
    {
        "resource_name": "raw_google_analytics_user_metrics_date",
        "dimensions": ["country", "city", "date"],
        "metrics": ["totalUsers", "newUsers", "userEngagementDuration"],
    },
]


@dlt_assets(
    dlt_source=google_analytics(queries=GA_QUERIES),
    dlt_pipeline=pipeline(
        pipeline_name="google_analytics",
        dataset_name=NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,  # schema
        destination="duckdb"
        if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev") == "dev"
        else "motherduck",
    ),
    name="google_analytics",
    # key_prefix=["raw"], # TODO: no prefixing yet
    group_name="raw_google_analytics",
    dlt_dagster_translator=GoogleAnalyticsDagsterDltTranslator(),
)
def google_analytics_dagster_assets(
    context: AssetExecutionContext, dlt: DagsterDltResource
):
    yield from dlt.run(context=context)


class NSWDOEDagsterDltTranslator(DagsterDltTranslator):
    @public
    def get_auto_materialize_policy(
        self, resource: DltResource
    ) -> Optional[AutoMaterializePolicy]:
        return AutoMaterializePolicy.eager().with_rules(
            AutoMaterializeRule.materialize_on_cron("0 0 * * *")
        )

    @public
    def get_asset_key(self, resource: DltResource) -> AssetKey:
        """Defines asset key for a given dlt resource key and dataset name.

        Args:
            resource (DltResource): dlt resource / transformer

        Returns:
            AssetKey of Dagster asset derived from dlt resource

        """
        return AssetKey(f"{resource.name}")

    @public
    def get_deps_asset_keys(self, resource: DltResource):  # -> Iterable[AssetKey]:
        """Defines upstream asset dependencies given a dlt resource.

        Defaults to a concatenation of `resource.source_name` and `resource.name`.

        Args:
            resource (DltResource): dlt resource / transformer

        Returns:
            # Iterable[AssetKey]: The Dagster asset keys upstream of `dlt_resource_key`.
            have set this to none, as DLT is usually the source, and dont want to complicate graph

        """
        # return [AssetKey(f"{resource.source_name}")] #[AssetKey(f"{resource.source_name}_{resource.name}")]


@dlt_assets(
    dlt_source=nsw_doe_enrolments(),
    dlt_pipeline=pipeline(
        pipeline_name="nsw_doe",
        dataset_name=NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,  # schema
        destination="duckdb"
        if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev") == "dev"
        else "motherduck",
    ),
    name="nsw_doe",
    # key_prefix=["raw"], # TODO: no prefixing yet
    group_name="raw_datahub",
    dlt_dagster_translator=NSWDOEDagsterDltTranslator(),
)
def raw__nsw_doe_datahub__enrolments(
    context: AssetExecutionContext, dlt: DagsterDltResource
):
    yield from dlt.run(context=context)
