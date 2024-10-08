{{
  config(
    materialized = 'table',

    )
}}

with

stg__order as (
    select * from {{ ref('stg__order') }}
),
date_prep as (

    {{ dbt_date.get_date_dimension('1992-01-01', '1998-12-31') }}


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
select * from final
{# {{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }} #}
{# from {{ ref('dim__date') }} where _meta__dim__date__sk = md5('-1') #}
