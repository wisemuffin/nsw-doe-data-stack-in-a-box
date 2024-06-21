with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datahub_early_childhood_education_centres') }}
),

renamed as (
    select
        {{ adapter.quote("location_id") }},
        {{ adapter.quote("id") }} as ece_centre_id,
        {{ adapter.quote("type_of_provider") }},
        {{ adapter.quote("provider_name") }},
        {{ adapter.quote("address") }},
        {{ adapter.quote("suburb") }},
        {{ adapter.quote("state") }},
        {{ adapter.quote("postcode") }},
        {{ adapter.quote("latitude") }},
        {{ adapter.quote("longitude") }},
        {{ adapter.quote("geo_data") }},
    {# {{ adapter.quote("_dlt_load_id") }}, #}
    {# {{ adapter.quote("_dlt_id") }} #}

    from source
)

{{ dbt_audit(
    cte_ref="renamed",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
