from typing import Any, Mapping, Optional

from dagster import AssetExecutionContext, AssetKey
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator, DagsterDbtTranslatorSettings

from ...constants import dbt_manifest_path

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    @classmethod
    def get_asset_key(cls, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        asset_key = super().get_asset_key(dbt_resource_props)

        if dbt_resource_props["resource_type"] == "source":
            # asset_key = asset_key.with_prefix("raw")
            pass
        else:
            asset_key = asset_key.with_prefix("nsw_doe")

        return asset_key
    def get_group_name(
        self, dbt_resource_props: Mapping[str, Any]
    ) -> Optional[str]:
        return "transformation"
    
@dbt_assets(manifest=dbt_manifest_path, dagster_dbt_translator=CustomDagsterDbtTranslator(settings=DagsterDbtTranslatorSettings(enable_asset_checks=True)),io_manager_key="io_manager_dw",exclude="*_saved_query")
def nsw_doe_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context ).stream()