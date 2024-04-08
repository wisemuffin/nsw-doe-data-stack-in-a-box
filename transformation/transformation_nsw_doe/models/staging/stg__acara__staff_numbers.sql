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
        {{ adapter.quote("Staff count") }} as "Staff_Count",
        {{ adapter.quote("_load_timestamp") }} as _load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),
final as (
    select *,{{ add_audit_columns() }}
    from renamed
)

select * from final
