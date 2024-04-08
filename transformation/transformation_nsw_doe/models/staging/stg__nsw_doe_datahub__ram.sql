with source as (
      select * from {{ source('raw', 'raw__nsw_doe_datahub__ram') }}
),
renamed as (
    select
        {{ adapter.quote("School Code") }} as "School_Code",
        {{ adapter.quote("School Full Name") }} as "School_Full_Name",
        {{ adapter.quote("Original RAM Funding $ ") }} as "Original_RAM_Funding_AUD",
        {{ adapter.quote("year") }} as "year",
        {{ adapter.quote("RAM Funding - post Adjustments $") }} as "RAM_Funding_post_Adjustments_AUD",
        {{ adapter.quote("Original RAM Funding $") }} as "Original_RAM_Funding_AUD",
        {{ adapter.quote("Sum of RAM Funding (incl oncosts) $") }} as "Sum_of_RAM_Funding_incl_oncosts_AUD",
        {{ adapter.quote(" Sum of RAM Funding (incl oncosts) $ ") }} as "_Sum_of_RAM_Funding_incl_oncosts_AUD",
        {{ adapter.quote("_load_timestamp") }} as _load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),
final as (
    select *,{{ add_audit_columns() }}
    from renamed
)

select * from final

  