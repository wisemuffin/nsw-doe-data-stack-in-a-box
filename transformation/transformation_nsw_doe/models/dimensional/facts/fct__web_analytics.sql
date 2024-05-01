{{ simple_cte([
    ('stg__google_analytics__user_metrics_date', 'stg__google_analytics__user_metrics_date')
]) }},
prep as (
    select *
    from stg__google_analytics__user_metrics_date
    where 1=1
),

final AS (

    SELECT 
        
        --Primary Key
        {{dbt_utils.generate_surrogate_key(['prep.date'])}} as _meta__fct__web_analytics__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions

        ----Local Dimensions
        country, 
        city, 
        date, 


        -- Measures
        total_users_integer as total_users,
        new_users_integer as new_users,
        user_engagement_duration_seconds


    FROM prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-30",
    updated_date="2024-04-30"
) }}

