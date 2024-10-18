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
from ...dlt_sources.nsw_doe import nsw_doe_data

from ...util.branching import set_schema_name_env

set_schema_name_env()

NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA", "schema_not_set"
)


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
    dlt_source=nsw_doe_data(),
    dlt_pipeline=pipeline(
        pipeline_name="nsw_doe",
        dataset_name=NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA,  # schema
        destination="duckdb"
        if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV", "dev") == "dev"
        else "motherduck",
    ),
    name="nsw_doe",
    # key_prefix=["raw"], # TODO: no prefixing yet
    group_name="raw_datansw",
    dlt_dagster_translator=NSWDOEDagsterDltTranslator(),
)
def raw__nsw_doe_data(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
