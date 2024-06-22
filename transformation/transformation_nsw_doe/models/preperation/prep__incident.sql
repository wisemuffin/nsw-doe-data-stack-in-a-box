with final as (
    select
        case_number,
        date_time_opened,
        term,
        incident_group,
        operational_directorate,
        principal_network_name,
        primary_category,
        summary_of_the_incident_external_distributionx,
        incident_priority_rating,
        incident_occurred,
        secondary_category,
        primary_sub_category,
    from {{ ref('stg__nsw_doe_datahub__incidents_2020_part_1') }}
    union all
    select
        case_number,
        date_time_opened,
        term,
        incident_group,
        operational_directorate,
        principal_network_name,
        primary_category,
        summary_of_the_incident_external_distributionx,
        incident_priority_rating,
        incident_occurred,
        secondary_category,
        primary_sub_category,
    from {{ ref('stg__nsw_doe_datahub__incidents_2020_part_2') }}
    union all
    select
        case_number,
        date_time_opened,
        term,
        incident_group,
        operational_directorate,
        principal_network_name,
        primary_category,
        summary_of_the_incident_external_distributionx,
        incident_priority_rating,
        incident_occurred,
        secondary_category,
        primary_sub_category,
    from {{ ref('stg__nsw_doe_datahub__incidents_2021_part_1') }}
    union all
    select
        case_number,
        date_time_opened,
        term,
        incident_group,
        operational_directorate,
        principal_network_name,
        primary_category,
        summary_of_the_incident_external_distributionx,
        incident_priority_rating,
        incident_occurred,
        secondary_category,
        primary_sub_category,
    from {{ ref('stg__nsw_doe_datahub__incidents_2021_part_2') }}
    union all
    select
        case_number,
        date_time_opened,
        term,
        incident_group,
        operational_directorate,
        principal_network_name,
        primary_category,
        summary_of_the_incident_external_distributionx,
        incident_priority_rating,
        incident_occurred,
        secondary_category,
        primary_sub_category,
    from {{ ref('stg__nsw_doe_datahub__incidents_2022_part_1') }}
    union all
    select
        case_number,
        date_time_opened,
        term,
        incident_group,
        operational_directorate,
        principal_network_name,
        primary_category,
        summary_of_the_incident_external_distributionx,
        incident_priority_rating,
        incident_occurred,
        secondary_category,
        primary_sub_category,
    from {{ ref('stg__nsw_doe_datahub__incidents_2022_part_2') }}
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
