with stg__datahub as (
    from {{ ref("stg__nsw_doe_datahub__master_dataset") }}
)
from stg__datahub