{{ config(
    post_hook=[
      "{{ missing_member_column(primary_key = '_meta__dim__school__sk', not_null_test_cols = []) }}"
    ]
) }}



with final as (

    select
        --Surrogate Key
        {{ dbt_utils.generate_surrogate_key(['School_Code']) }}
            as _meta__dim__school__sk,


        --Natural Key
        school_code,

        --School Information
        age_id,
        school_name,
        street,
        town_suburb,
        postcode,
        phone,
        school_email,
        website,
        fax,
        latest_year_enrolment_fte,
        indigenous_pct,
        lbote_pct,
        icsea_value,
        level_of_schooling,
        selective_school,
        opportunity_class,
        school_specialty_type,
        school_subtype,
        support_classes,
        preschool_ind,
        distance_education,
        intensive_english_centre,
        school_gender,
        late_opening_school,
        date_1st_teacher,
        lga,
        electorate_from_2023,
        electorate_2015_2022,
        fed_electorate,
        operational_directorate,
        principal_network,
        operational_directorate_office,
        operational_directorate_office_phone,
        operational_directorate_office_address,
        facs_district,
        local_health_district,
        aecg_region,
        asgs_remoteness,
        latitude,
        longitude,
        assets_unit,
        sa4,
    {# "Date_Extracted", #}
    {# "_load_source_timestamp", #}
    {# "_source", #}

    from {{ ref('prep__school') }}

)



{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
