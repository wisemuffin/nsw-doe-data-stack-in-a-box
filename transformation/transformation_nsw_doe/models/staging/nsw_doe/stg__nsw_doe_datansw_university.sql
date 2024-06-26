with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datansw_university') }}
),

renamed as (
    select
        {{ adapter.quote("uni_id") }},
        {{ adapter.quote("uni_campus_id") }},
        {{ adapter.quote("university_name") }},
        {{ adapter.quote("university_campus_name") }},
        {{ adapter.quote("address") }},
        {{ adapter.quote("street") }},
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

select *, from renamed
