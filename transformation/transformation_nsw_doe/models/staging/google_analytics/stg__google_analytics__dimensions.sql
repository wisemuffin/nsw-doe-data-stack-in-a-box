with source as (
    select *, from {{ source('raw', 'raw_google_analytics_dimensions') }}
),

renamed as (
    select
        {{ adapter.quote("api_name") }},
        {{ adapter.quote("ui_name") }},
        {{ adapter.quote("description") }},
        {{ adapter.quote("category") }},
        {{ adapter.quote("_dlt_load_id") }},
        {{ adapter.quote("_dlt_id") }}

    from source
)

select *, from renamed
