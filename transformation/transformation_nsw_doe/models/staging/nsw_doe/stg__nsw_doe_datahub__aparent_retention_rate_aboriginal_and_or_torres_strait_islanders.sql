with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datahub_aparent_retention_rate_aboriginal_and_or_torres_strait_islanders') }}
),

renamed as (
    select
        {{ adapter.quote("retention_period") }},
        {{ adapter.quote("_2019xx") }},
        {{ adapter.quote("_2020_old_methodologyxx") }},
        {{ adapter.quote("_2020_new_methodologyxx") }},
        {{ adapter.quote("_2021xx") }},
        {{ adapter.quote("_2022xx") }},
        {{ adapter.quote("_2023xx") }}
    {# {{ adapter.quote("_dlt_load_id") }}, #}
    {# {{ adapter.quote("_dlt_id") }} #}

    from source
),

unpivoted as (
    unpivot renamed
    on columns(* exclude (retention_period))
    into
    name year
    value aparent_retention_rate_aboriginal_and_or_torres_strait_islanders
),

final as (
    select
        retention_period,
        cast(substring(year, 2, 4) as INTEGER) as calendar_year,
        cast(aparent_retention_rate_aboriginal_and_or_torres_strait_islanders as DECIMAL) as aparent_retention_rate_aboriginal_and_or_torres_strait_islanders,
    from unpivoted
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
