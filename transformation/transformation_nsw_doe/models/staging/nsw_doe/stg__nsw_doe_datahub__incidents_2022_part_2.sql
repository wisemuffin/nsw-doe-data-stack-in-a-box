with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datahub_incidents_2022_part_2') }}
),

renamed as (
    select
        {{ adapter.quote("case_number") }},
        {{ adapter.quote("date_time_opened") }},
        {{ adapter.quote("term") }},
        {{ adapter.quote("incident_group") }},
        {{ adapter.quote("operational_directorate") }},
        {{ adapter.quote("principal_network_name") }},
        {{ adapter.quote("primary_category") }},
        {{ adapter.quote("incident_priority_rating") }},
        {{ adapter.quote("incident_occurred") }},
        {{ adapter.quote("summary_of_the_incident_external_distributionx") }},
        {{ adapter.quote("secondary_category") }},
        {{ adapter.quote("primary_sub_category") }},
    {# {{ adapter.quote("_dlt_load_id") }}, #}
    {# {{ adapter.quote("_dlt_id") }}, #}

    from source
)

{{ dbt_audit(
    cte_ref="renamed",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
