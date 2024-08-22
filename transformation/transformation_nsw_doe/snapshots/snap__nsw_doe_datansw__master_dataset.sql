{% snapshot snap__nsw_doe_datansw__master_dataset_snapshot %}

{{
    config(
      target_schema=env_var('NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA'),
      unique_key='School_code',

      invalidate_hard_deletes=True,
      strategy='check',
      check_cols=["School_code","AgeID","School_name","Street","Town_suburb","Postcode","Phone","School_Email","Website","Fax","latest_year_enrolment_FTE","Indigenous_pct","LBOTE_pct","ICSEA_value","Level_of_schooling","Selective_school","Opportunity_class","School_specialty_type","School_subtype","Support_classes","Preschool_ind","Distance_education","Intensive_english_centre","School_gender","Late_opening_school","Date_1st_teacher","LGA","electorate_from_2023","electorate_2015_2022","Fed_electorate","Operational_directorate","Principal_network","Operational_directorate_office","Operational_directorate_office_phone","Operational_directorate_office_address","FACS_district","Local_health_district","AECG_region","ASGS_remoteness","Latitude","Longitude","SA4","FOEI_Value"],

    )
}}

    select *, from {{ source('raw', 'raw__nsw_doe_datansw__master_dataset') }}

{% endsnapshot %}
