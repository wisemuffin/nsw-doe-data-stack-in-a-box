{{ config(
    post_hook=[
      "{{ missing_member_column(primary_key = '_meta__dim__school__sk', not_null_test_cols = []) }}"
    ]
) }}



WITH final AS (

    SELECT 
        --Surrogate Key
        {{dbt_utils.generate_surrogate_key(['School_Code'])}} as _meta__dim__school__sk,


        --Natural Key
        "School_Code",

        --School Information
        "Age_ID",
        "School_Name",
        "Street",
        "Town_Suburb",
        "Postcode",
        "Phone",
        "School_Email",
        "Website",
        "Fax",
        "Latest_Year_Enrolment_FTE",
        "Indigenous_pct",
        "LBOTE_pct",
        "ICSEA_value",
        "Level_of_Schooling",
        "Selective_school",
        "Opportunity_class",
        "School_specialty_type",
        "School_Subtype",
        "Support_Classes",
        "Preschool_ind",
        "Distance_Education",
        "Intensive_English_Centre",
        "School_Gender",
        "Late_Opening_School",
        "Date_1st_Teacher",
        "LGA",
        "Electorate_from_2023",
        "Electorate_2015_2022",
        "Fed_electorate",
        "Operational_directorate",
        "Principal_network",
        "Operational_directorate_office",
        "Operational_directorate_office_phone",
        "Operational_directorate_office_address",
        "FACS_district",
        "Local_health_district",
        "AECG_Region",
        "ASGS_Remoteness",
        "Latitude",
        "Longitude",
        "Assets_Unit",
        "SA4"
        {# "Date_Extracted", #}
        {# "_load_source_timestamp", #}
        {# "_source", #}

    FROM {{ ref('prep__school') }}

)



{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}