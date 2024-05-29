from typing import Any, Mapping, Optional

from dagster import AssetExecutionContext, AssetKey
from dagster_dbt import (
    DagsterDbtTranslator,
    DagsterDbtTranslatorSettings,
    DbtCliResource,
    dbt_assets,
)

from ...project import nsw_doe_data_stack_in_a_box_project


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        asset_key = super().get_asset_key(dbt_resource_props)

        if dbt_resource_props["resource_type"] == "source":
            # asset_key = asset_key.with_prefix("raw")
            pass
        else:
            asset_key = asset_key.with_prefix("nsw_doe")

        return asset_key

    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        return "transformation"


@dbt_assets(
    manifest=nsw_doe_data_stack_in_a_box_project.manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(
        settings=DagsterDbtTranslatorSettings(
            enable_asset_checks=True, enable_duplicate_source_asset_keys=True
        )
    ),
    io_manager_key="io_manager_dw",
    exclude="saved_query:* *google* *github* *web_analytics* *repo*",
    select="fqn:*",
    # select="fqn:* fqn:*" # works
    # select="fqn:* tag:api" # not working
    # select="tag:api" # not working
    # select="tag:all" # not working
    # select="*google* *github* *web_analytics* *repo*" # works
    # select="nsw_doe_data_stack_in_a_box.staging* nsw_doe_data_stack_in_a_box.dimensional*"
)
def nsw_doe_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


class CustomDagsterDbtTranslatorAPIRequired(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        asset_key = super().get_asset_key(dbt_resource_props)

        if dbt_resource_props["resource_type"] == "source":
            # asset_key = asset_key.with_prefix("raw")
            pass
        else:
            asset_key = asset_key.with_prefix("nsw_doe")

        return asset_key

    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        return "transformation_requires_api"


@dbt_assets(
    manifest=nsw_doe_data_stack_in_a_box_project.manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslatorAPIRequired(
        settings=DagsterDbtTranslatorSettings(
            enable_asset_checks=True, enable_duplicate_source_asset_keys=True
        )
    ),
    io_manager_key="io_manager_dw",
    exclude="saved_query:*",
    select="*google* *github* *web_analytics* *repo*",
    # select="fqn:* fqn:*" # works
    # select="fqn:* tag:api" # not working
    # select="tag:api" # not working
    # select="tag:all" # not working
    # select="*google* *github* *web_analytics* *repo*" # works
    # select="nsw_doe_data_stack_in_a_box.staging* nsw_doe_data_stack_in_a_box.dimensional*"
)
def nsw_doe_dbt_assets_requires_api(
    context: AssetExecutionContext, dbt: DbtCliResource
):
    yield from dbt.cli(["build"], context=context).stream()
