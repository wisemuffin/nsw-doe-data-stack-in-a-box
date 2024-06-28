from dagster import asset

from ..semantic_layer.assets import (
    metrics_by_year_saved_query_s3,
    metrics_by_year_school_saved_query_s3,
)


@asset(
    compute_kind="tableau",
    group_name="reporting",
    deps=[metrics_by_year_saved_query_s3, metrics_by_year_school_saved_query_s3],
)
def tableau_dashboard__experimental():
    """
    🚧 to work on setting up automated refresh of cache on tableau public
    """
    pass


@asset(
    compute_kind="powerbi",
    group_name="reporting",
    deps=[metrics_by_year_saved_query_s3, metrics_by_year_school_saved_query_s3],
)
def powerbi_dashboard__experimental():
    """
    🚧 to work on setting up automated refresh of cache on power bi
    """
    pass
