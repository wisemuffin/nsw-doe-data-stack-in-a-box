{{ simple_cte([
    ('stg__github_reactions__issues_reactions', 'stg__github_reactions__issues_reactions'),
    ('stg__github_reactions__issues', 'stg__github_reactions__issues')
]) }},
prep as (
    select content, sum(1)
    from stg__github_reactions__issues_reactions
    where 1=1
    group by content
),

final AS (

    SELECT 
        
        --Primary Key
        {{dbt_utils.generate_surrogate_key(['prep.date'])}} as _meta__fct__web_analytics__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions

        ----Local Dimensions


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

