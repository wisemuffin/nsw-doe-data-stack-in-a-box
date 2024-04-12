with source as (
      select * from {{ source('raw', 'raw__nsw_doe_datahub__ram') }}
),
renamed as (
    select
        {{ adapter.quote("School Code") }} as "School_Code",
        {{ adapter.quote("School Full Name") }} as "School_Full_Name",
        TRY_CAST(REPLACE(REPLACE({{ adapter.quote("Original RAM Funding $ ") }} , '$', ''), ',', '') AS INTEGER) as "Original_RAM_Funding_AUD",
        {{ adapter.quote("year") }} as "year",
        TRY_CAST(REPLACE(REPLACE({{ adapter.quote("RAM Funding - post Adjustments $") }} , '$', ''), ',', '') AS INTEGER) as "RAM_Funding_post_Adjustments_AUD",
        TRY_CAST(REPLACE(REPLACE({{ adapter.quote("Original RAM Funding $") }} , '$', ''), ',', '') AS INTEGER) as "Original_RAM_Funding_AUD",
        TRY_CAST(REPLACE(REPLACE({{ adapter.quote("Sum of RAM Funding (incl oncosts) $") }} , '$', ''), ',', '') AS INTEGER) as "Sum_of_RAM_Funding_incl_oncosts_AUD",
        TRY_CAST(REPLACE(REPLACE({{ adapter.quote(" Sum of RAM Funding (incl oncosts) $ ") }} , '$', ''), ',', '') AS INTEGER) as "_Sum_of_RAM_Funding_incl_oncosts_AUD",
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
