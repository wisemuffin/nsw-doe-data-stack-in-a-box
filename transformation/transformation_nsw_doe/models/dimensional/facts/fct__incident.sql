with prep__incident as (
    from {{ ref('prep__incident') }}
),

final as (

    select
        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep__incident.case_number']) }}
            as _meta__fct__school__sk,

        --Natural Key
        prep__incident.case_number,

        --Foreign Keys
        ----Conformed Dimensions


        ----Local Dimensions
        prep__incident.date_time_opened,
        prep__incident.primary_category,
        prep__incident.summary_of_the_incident_external_distributionx,
        prep__incident.incident_priority_rating,
        prep__incident.incident_occurred,
        prep__incident.secondary_category,
        prep__incident.primary_sub_category,


        -- Measures
        1 as incidents,


    from prep__incident
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
