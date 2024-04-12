with source as (
      select * from {{ source('raw', 'raw__nsw_doe_datahub__master_dataset') }}
),
renamed as (
    select
        {{ adapter.quote("School_code") }} as "School_Code",
        {{ adapter.quote("AgeID") }} as "Age_ID",
        {{ adapter.quote("School_name") }} as "School_Name",
        {{ adapter.quote("Street") }} as "Street",
        {{ adapter.quote("Town_suburb") }} as "Town_Suburb",
        {{ adapter.quote("Postcode") }} as "Postcode",
        {{ adapter.quote("Phone") }} as "Phone",
        {{ adapter.quote("School_Email") }} as "School_Email",
        {{ adapter.quote("Website") }} as "Website",
        {{ adapter.quote("Fax") }} as "Fax",
        {{ adapter.quote("latest_year_enrolment_FTE") }} as "Latest_Year_Enrolment_FTE",
        {{ adapter.quote("Indigenous_pct") }} as "Indigenous_pct",
        {{ adapter.quote("LBOTE_pct") }} as "LBOTE_pct",
        {{ adapter.quote("ICSEA_value") }} as "ICSEA_value",
        {{ adapter.quote("Level_of_schooling") }} as "Level_of_Schooling",
        {{ adapter.quote("Selective_school") }} as "Selective_school",
        {{ adapter.quote("Opportunity_class") }} as "Opportunity_class",
        {{ adapter.quote("School_specialty_type") }} as "School_specialty_type",
        {{ adapter.quote("School_subtype") }} as "School_Subtype",
        {{ adapter.quote("Support_classes") }} as "Support_Classes",
        {{ adapter.quote("Preschool_ind") }} as "Preschool_ind",
        {{ adapter.quote("Distance_education") }} as "Distance_Education",
        {{ adapter.quote("Intensive_english_centre") }} as "Intensive_English_Centre",
        {{ adapter.quote("School_gender") }} as "School_Gender",
        {{ adapter.quote("Late_opening_school") }} as "Late_Opening_School",
        {{ adapter.quote("Date_1st_teacher") }} as "Date_1st_Teacher",
        {{ adapter.quote("LGA") }} as "LGA",
        {{ adapter.quote("electorate_from_2023") }} as "Electorate_from_2023",
        {{ adapter.quote("electorate_2015_2022") }} as "Electorate_2015_2022",
        {{ adapter.quote("Fed_electorate") }} as "Fed_electorate",
        {{ adapter.quote("Operational_directorate") }} as "Operational_directorate",
        {{ adapter.quote("Principal_network") }} as "Principal_network",
        {{ adapter.quote("Operational_directorate_office") }} as "Operational_directorate_office",
        {{ adapter.quote("Operational_directorate_office_phone") }} as "Operational_directorate_office_phone",
        {{ adapter.quote("Operational_directorate_office_address") }} as "Operational_directorate_office_address",
        {{ adapter.quote("FACS_district") }} as "FACS_district",
        {{ adapter.quote("Local_health_district") }} as "Local_health_district",
        {{ adapter.quote("AECG_region") }} as "AECG_Region",
        {{ adapter.quote("ASGS_remoteness") }} as "ASGS_Remoteness",
        {{ adapter.quote("Latitude") }} as "Latitude",
        {{ adapter.quote("Longitude") }} as "Longitude",
        {{ adapter.quote("Assets unit") }} as "Assets_Unit",
        {{ adapter.quote("SA4") }} as "SA4",
        {{ adapter.quote("Date_extracted") }} as _meta__load_source_timestamp,
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