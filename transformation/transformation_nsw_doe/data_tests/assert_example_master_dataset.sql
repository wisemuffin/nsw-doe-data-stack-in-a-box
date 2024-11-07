select *, from {{ ref('stg__nsw_doe_datansw__master_dataset') }} where School_code < 9000
