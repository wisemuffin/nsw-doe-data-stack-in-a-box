with source as (
    select *, from {{ source('raw', 'raw__acara__staff_numbers') }}
),

renamed as (
    select
        {{ adapter.quote("Calendar Year") }} as calendar_year,
        {{ adapter.quote("State/territory") }} as state_territory,
        {{ adapter.quote("School sector") }} as school_sector,
        {{ adapter.quote("School level") }} as school_level,
        {{ adapter.quote("Staff function") }} as staff_function,
        {{ adapter.quote("Sex/gender") }} as sex_gender,
        {{ adapter.quote("FTE Status") }} as fte_status,
        REPLACE({{ adapter.quote("Staff count") }}, ',', '')::DECIMAL(16, 2)
            as staff_count,
        {{ adapter.quote("_load_timestamp") }} as _meta__load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),

final as (
    select *,
    from renamed
    where 1 = 1
    -- removing aggregates from files
    and school_sector != 'All non-government'
    and school_level != 'All'
    and staff_function != 'All staff'
    and sex_gender != 'All'
    and staff_function != 'All non-teaching staff'
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
