with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datansw_aparent_retention_rate_10_to_12') }}
),

renamed as (
    select
        {{ adapter.quote("sa4_groups") }},
        {{ adapter.quote("_2014xx") }},
        {{ adapter.quote("_2015xx") }},
        {{ adapter.quote("_2016xx") }},
        {{ adapter.quote("_2017xx") }},
        {{ adapter.quote("_2018xx") }},
        {{ adapter.quote("_2019xx") }},
        {{ adapter.quote("_2020_old_methodologyxx") }},
        {{ adapter.quote("_2020_new_methodologyxx") }},
        {{ adapter.quote("_2021xx") }},
        {{ adapter.quote("_2022xx") }},
        {{ adapter.quote("_2023xx") }},
        {{ adapter.quote("_dlt_load_id") }},
        {{ adapter.quote("_dlt_id") }}

    from source
),

unpivoted as (
    unpivot renamed
    on columns(* exclude (sa4_groups, _dlt_load_id, _dlt_id))
    into
    name year
    value aparent_retention_rate_10_to_12
),

final as (
    select
        sa4_groups,
        cast(substring(year, 2, 4) as INTEGER) as calendar_year,
        cast(aparent_retention_rate_10_to_12 as DECIMAL) as aparent_retention_rate_10_to_12,
    from unpivoted
)

  {{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
