with source as (
    select *, from {{ source('raw', 'raw__nsw_doe_datahub__apprenticeship_traineeship_training_contract_approvals') }}
),

renamed as (
    select
        {# {{ adapter.quote("Unnamed: 0") }}, #}
        {{ adapter.quote("Training Type") }} as training_type,
        {{ adapter.quote("     2024") }},
        {{ adapter.quote("     2023") }},
        {{ adapter.quote("     2022") }},
        {{ adapter.quote("     2021") }},
        {{ adapter.quote("     2020") }},
        {{ adapter.quote("     2019") }},
        {{ adapter.quote("     2018") }},
        {{ adapter.quote("     2017") }},
        {{ adapter.quote("     2016") }},
        {{ adapter.quote("     2015") }},
    {# {{ adapter.quote("_load_timestamp") }}, #}
    {# {{ adapter.quote("_source") }} #}

    from source
),

unpivoted as (
    unpivot renamed
    on columns(* exclude (training_type))
    into
    name year
    value apprenticeship_traineeship_training_contract_approvals
),

final as (
    select
        training_type,
        cast(substring(year, 6, 8) as INTEGER) as calendar_year,
        cast(replace(apprenticeship_traineeship_training_contract_approvals, ',', '') as INT) as apprenticeship_traineeship_training_contract_approvals,
    from unpivoted
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
