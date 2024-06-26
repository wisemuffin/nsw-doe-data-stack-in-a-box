with stg__nsw_doe_datansw__aparent_retention_rate_7_to_10 as (
    select *, from {{ ref('stg__nsw_doe_datansw__aparent_retention_rate_7_to_10') }}
),

stg__nsw_doe_datansw__aparent_retention_rate_10_to_12 as (
    from {{ ref('stg__nsw_doe_datansw__aparent_retention_rate_10_to_12') }}
),

prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders as (
    from {{ ref('prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders') }}
),

all_years as (
    select calendar_year,
    from stg__nsw_doe_datansw__aparent_retention_rate_7_to_10
    union
    select calendar_year,
    from stg__nsw_doe_datansw__aparent_retention_rate_10_to_12
    union
    select calendar_year,
    from prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders
),

prep as (
    -- keeping these metrics at state level as cant aggregate from sa4 to state
    select
        all_years.calendar_year,
        stg__nsw_doe_datansw__aparent_retention_rate_7_to_10.aparent_retention_rate_7_to_10,
        stg__nsw_doe_datansw__aparent_retention_rate_10_to_12.aparent_retention_rate_10_to_12,
        prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders.aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders,
        prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders.aparent_retention_rate_7_to_10_aboriginal_and_or_torres_strait_islanders,
        prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders.aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders,
    from all_years
    left join stg__nsw_doe_datansw__aparent_retention_rate_7_to_10 on all_years.calendar_year = stg__nsw_doe_datansw__aparent_retention_rate_7_to_10.calendar_year
    left join stg__nsw_doe_datansw__aparent_retention_rate_10_to_12 on all_years.calendar_year = stg__nsw_doe_datansw__aparent_retention_rate_10_to_12.calendar_year
    left join prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders on all_years.calendar_year = prep_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders.calendar_year
    where stg__nsw_doe_datansw__aparent_retention_rate_7_to_10.sa4_groups = 'NSW'
),

final as (

    select

        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep.calendar_year']) }}
            as _meta__fct__retention__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions
        {# prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force  #}

        ----Local Dimensions
        prep.calendar_year,
        cast((prep.calendar_year || '-01-01') as date) as calendar_date, -- this is ugly 🚧 TODO, required for dbt metrics layer


        -- Measures
        prep.aparent_retention_rate_7_to_10 / 100 as aparent_retention_rate_7_to_10,
        prep.aparent_retention_rate_10_to_12 / 100 as aparent_retention_rate_10_to_12,
        prep.aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders / 100 as aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders,
        prep.aparent_retention_rate_7_to_10_aboriginal_and_or_torres_strait_islanders / 100 as aparent_retention_rate_7_to_10_aboriginal_and_or_torres_strait_islanders,
        prep.aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders / 100 as aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders,


    from prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
