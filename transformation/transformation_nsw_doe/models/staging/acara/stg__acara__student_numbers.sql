with source as (
      select * from {{ source('raw', 'raw__acara__student_numbers') }}
),
renamed as (
    select
        {{ adapter.quote("Calendar Year") }} as "Calendar_Year",
        {{ adapter.quote("State/territory") }} as "State_Territory",
        {{ adapter.quote("School sector") }} as "School_Sector",
        {{ adapter.quote("School level") }} as "School_Level",
        {{ adapter.quote("Sex/gender") }} as "Sex_Gender",
        {{ adapter.quote("Aboriginal or Torres Strait Islander status") }} as "Aboriginal_Or_Torres_Strait_Islander_Status",
        {{ adapter.quote("Full-time/part-time status") }} as "Full_Time_Part_Time_Status",
        {{ adapter.quote("Student count") }} as "Student_Count",
        {{ adapter.quote("Proportion of sector") }} as "Proportion_Of_Sector",
        {{ adapter.quote("Proportion of state") }} as "Proportion_Of_State",
        {{ adapter.quote("Proportion of school level") }} as "Proportion_Of_School_Level",
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
  