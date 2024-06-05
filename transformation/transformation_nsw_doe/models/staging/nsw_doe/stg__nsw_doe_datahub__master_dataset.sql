with source as (
    select *, from {{ source('raw', 'raw__nsw_doe_datahub__master_dataset') }}
),

renamed as (
    select
        {{ adapter.quote("School_code") }},
        {{ adapter.quote("AgeID") }} as age_id,
        {{ adapter.quote("School_name") }},
        {{ adapter.quote("Street") }},
        {{ adapter.quote("Town_suburb") }},
        {{ adapter.quote("Postcode") }},
        {{ adapter.quote("Phone") }},
        {{ adapter.quote("School_Email") }},
        {{ adapter.quote("Website") }},
        {{ adapter.quote("Fax") }},
        {{ adapter.quote("latest_year_enrolment_FTE") }},
        {{ adapter.quote("Indigenous_pct") }},
        {{ adapter.quote("LBOTE_pct") }},
        {{ adapter.quote("ICSEA_value") }},
        {{ adapter.quote("Level_of_schooling") }},
        {{ adapter.quote("Selective_school") }},
        {{ adapter.quote("Opportunity_class") }},
        {{ adapter.quote("School_specialty_type") }},
        {{ adapter.quote("School_subtype") }},
        {{ adapter.quote("Support_classes") }},
        {{ adapter.quote("Preschool_ind") }},
        {{ adapter.quote("Distance_education") }},
        {{ adapter.quote("Intensive_english_centre") }},
        {{ adapter.quote("School_gender") }},
        {{ adapter.quote("Late_opening_school") }},
        {{ adapter.quote("Date_1st_teacher") }},
        {{ adapter.quote("LGA") }},
        {{ adapter.quote("electorate_from_2023") }},
        {{ adapter.quote("electorate_2015_2022") }},
        {{ adapter.quote("Fed_electorate") }},
        {{ adapter.quote("Operational_directorate") }},
        {{ adapter.quote("Principal_network") }},
        {{ adapter.quote("Operational_directorate_office") }},
        {{ adapter.quote("Operational_directorate_office_phone") }},
        {{ adapter.quote("Operational_directorate_office_address") }},
        {{ adapter.quote("FACS_district") }},
        {{ adapter.quote("Local_health_district") }},
        {{ adapter.quote("AECG_region") }},
        {{ adapter.quote("ASGS_remoteness") }},
        {{ adapter.quote("Latitude") }},
        {{ adapter.quote("Longitude") }},
        {{ adapter.quote("Assets unit") }} as assets_unit,
        {{ adapter.quote("SA4") }},
        {{ adapter.quote("Date_extracted") }}::date
            as _meta__load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),

final as (
    select *,
    from renamed
)


  {{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
