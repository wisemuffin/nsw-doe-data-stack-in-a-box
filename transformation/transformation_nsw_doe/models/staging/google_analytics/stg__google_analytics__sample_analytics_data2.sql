with source as (
    select *, from {{ source('raw', 'raw_google_analytics_sample_analytics_data2') }}
),

renamed as (
    select
        {{ adapter.quote("browser") }},
        {{ adapter.quote("city") }},
        {{ adapter.quote("date_hour") }},
        {{ adapter.quote("date") }},
        {{ adapter.quote("total_users_integer") }},
        {{ adapter.quote("_dlt_load_id") }},
        {{ adapter.quote("_dlt_id") }}

    from source
)

select *, from renamed
