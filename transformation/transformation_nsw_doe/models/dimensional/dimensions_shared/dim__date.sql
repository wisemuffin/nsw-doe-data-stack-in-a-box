{{
  config(
    materialized = 'table',
    post_hook=["{{ missing_member_column(primary_key = '_meta__dim__date__sk') }}"]

    )
}}

with

date_prep as (

    {{ dbt_date.get_date_dimension('2023-01-01', '2027-12-31') }}


),

final as (
    select
        -- Surrogate Key
        -- its bit over kill to make every date in a fact table require a SK.
        -- Lets just join on the natural key yyyy-mm-dd?
        {{ dbt_utils.generate_surrogate_key(['date_day']) }} as _meta__dim__date__sk,
        {# date_day as _meta__dim__date__sk, #}

        --Date Information
        *,
        1 as test,
    from date_prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
{# from {{ ref('dim__date') }} where _meta__dim__date__sk = md5('-1') #}
