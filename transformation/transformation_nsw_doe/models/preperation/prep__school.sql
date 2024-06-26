with final as (
    select
    {{ dbt_utils.star(
           from=ref('stg__nsw_doe_datansw__master_dataset'),
           except=['_audit__created_by','_audit__updated_by','_audit__model_created_date','_audit__model_updated_date','_audit__dbt_updated_at','_audit__dbt_created_at']
           )
      }}
    from {{ ref("stg__nsw_doe_datansw__master_dataset") }}
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
