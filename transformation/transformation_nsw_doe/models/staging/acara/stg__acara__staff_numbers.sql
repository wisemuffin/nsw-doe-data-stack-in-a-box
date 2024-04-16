with source as (
      select * from {{ source('raw', 'raw__acara__staff_numbers') }}
),
renamed as (
    select
        {{ adapter.quote("Calendar Year") }} as "Calendar_Year",
        {{ adapter.quote("State/territory") }} as "State_Territory",
        {{ adapter.quote("School sector") }} as "School_Sector",
        {{ adapter.quote("School level") }} as "School_Level",
        {{ adapter.quote("Staff function") }} as "Staff_Function",
        {{ adapter.quote("Sex/gender") }} as "Sex_Gender",
        {{ adapter.quote("FTE Status") }} as "FTE_Status",
        REPLACE({{ adapter.quote("Staff count") }}, ',', '')::DECIMAL(16, 2) as "Staff_Count",
        {{ adapter.quote("_load_timestamp") }} as _meta__load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),
final as (
    select *
    from renamed
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}