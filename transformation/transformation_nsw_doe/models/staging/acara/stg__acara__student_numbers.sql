with source as (
    select *, from {{ source('raw', 'raw__acara__student_numbers') }}
),

renamed as (
    select
        {{ adapter.quote("Calendar Year") }} as calendar_year,
        {{ adapter.quote("State/territory") }} as state_territory,
        {{ adapter.quote("School sector") }} as school_sector,
        {{ adapter.quote("School level") }} as school_level,
        {{ adapter.quote("Sex/gender") }} as sex_gender,
        {{ adapter.quote("Aboriginal or Torres Strait Islander status") }}
            as aboriginal_or_torres_strait_islander_status,
        {{ adapter.quote("Full-time/part-time status") }}
            as full_time_part_time_status,
        REPLACE({{ adapter.quote("Student count") }}, ',', '')::DECIMAL(16, 2)
            as student_count,
        {{ adapter.quote("Proportion of sector") }} as proportion_of_sector,
        {{ adapter.quote("Proportion of state") }} as proportion_of_state,
        {{ adapter.quote("Proportion of school level") }}
            as proportion_of_school_level,
        {{ adapter.quote("_load_timestamp") }} as _meta__load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),

final as (
    select *,
    from renamed
    where 1 = 1
    -- removing aggregates from files
    and school_sector != 'All'
    and school_level in ('Primary', 'Secondary')
    and sex_gender != 'All'
    and aboriginal_or_torres_strait_islander_status != 'All'
    and full_time_part_time_status != 'All'
    and full_time_part_time_status != 'Full-time equivalent'
)

  {{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
