import os
from dagster_tableau import (
    TableauCloudWorkspace,
    # build_tableau_materializable_assets_definition, # waiting on dagster 1.9.0
    # load_tableau_asset_specs,   # waiting on dagster 1.9.0
    # parse_tableau_external_and_materializable_asset_specs,  # waiting on dagster 1.9.0
)

# from ... import power_bi_resource


# power_bi_resource.build_defs(enable_refresh_semantic_models=True)


# Connect to Tableau Cloud using the connected app credentials
tableau_workspace = TableauCloudWorkspace(
    connected_app_client_id=os.getenv("TABLEAU_CONNECTED_APP_CLIENT_ID", ""),
    connected_app_secret_id=os.getenv("TABLEAU_CONNECTED_APP_SECRET_ID", ""),
    connected_app_secret_value=os.getenv("TABLEAU_CONNECTED_APP_SECRET_VALUE", ""),
    username=os.getenv("TABLEAU_USERNAME", ""),
    site_name=os.getenv("TABLEAU_SITE_NAME", ""),
    pod_name=os.getenv("TABLEAU_POD_NAME", ""),
)


# # power_bi_resource = PowerBIWorkspace(
# #     credentials=PowerBIServicePrincipal(
# #         client_id=os.getenv("POWER_BI_CLIENT_ID",""),
# #         client_secret=os.getenv("POWER_BI_CLIENT_SECRET",""),
# #         tenant_id=os.getenv("POWER_BI_TENANT_ID",""),
# #     ),
# #     workspace_id=os.getenv("POWER_BI_WORKSPACE_ID",""),
# # )
