{{ simple_cte([
    ('stg__github_reactions__issues_reactions', 'stg__github_reactions__issues_reactions'),
    ('stg__github_reactions__issues', 'stg__github_reactions__issues')
]) }},
prep as (
    select content, created_at::date as date, sum(1) as cnt_reaction
    from stg__github_reactions__issues_reactions
    where 1=1
    group by all
),
final AS (

    SELECT

        --Primary Key
        {{dbt_utils.generate_surrogate_key(['prep.date', 'prep.content'])}} as _meta__fct__repo_issue_reaction__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions

        ----Local Dimensions
        prep.content,
        prep.date,


        -- Measures
        prep.cnt_reaction


    FROM prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-30",
    updated_date="2024-04-30"
) }}
