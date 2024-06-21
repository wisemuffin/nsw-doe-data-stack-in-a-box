with stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals as (
    from {{ ref('stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals') }}
),

stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions as (
    from {{ ref('stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions') }}
),

all_years as (
    select
        calendar_year,
        training_type,
    from stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals
    union
    select
        calendar_year,
        training_type,
    from stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions
),

prep as (
    -- keeping these metrics at state level as cant aggregate from sa4 to state
    select
        all_years.calendar_year,
        all_years.training_type,
        stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals.apprenticeship_traineeship_training_contract_approvals,
        stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions.apprenticeship_traineeship_training_contract_completions,
    from all_years
    left join stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals
        on
            all_years.calendar_year = stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals.calendar_year
            and all_years.training_type = stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals.training_type
    left join stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions on
        all_years.calendar_year = stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions.calendar_year
        and all_years.training_type = stg__nsw_doe_datahub__apprenticeship_traineeship_training_contract_completions.training_type
),

final as (

    select

        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep.calendar_year', 'prep.training_type']) }}
            as _meta__fct__apprenticeship_traineeship_training__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions
        {# prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force  #}

        ----Local Dimensions
        prep.calendar_year,
        prep.training_type,


        -- Measures
        prep.apprenticeship_traineeship_training_contract_approvals,
        prep.apprenticeship_traineeship_training_contract_completions,


    from prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
