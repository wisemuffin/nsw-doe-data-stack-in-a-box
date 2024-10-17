with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datansw_class_size') }}
),

renamed as (
    select
        {# {{ adapter.quote("_dlt_load_id") }}, #}
        {# {{ adapter.quote("_dlt_id") }}, #}
        cast({{ adapter.quote("year") }} as int) as calendar_year,
        cast({{ adapter.quote("k") }} as decimal) as k,
        cast({{ adapter.quote("year_1") }} as decimal) as year_1,
        cast({{ adapter.quote("year_2") }} as decimal) as year_2,
        cast({{ adapter.quote("year_3") }} as decimal) as year_3,
        cast({{ adapter.quote("year_4") }} as decimal) as year_4,
        cast({{ adapter.quote("year_5") }} as decimal) as year_5,
        cast({{ adapter.quote("year_6") }} as decimal) as year_6,
        cast({{ adapter.quote("k_6") }} as decimal) as k_6,
        1 as dave,

    from source
    where year not in ('Year', '-') --api pulls doesn correctly start at header

),

final as (
    select *,
    from renamed
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
