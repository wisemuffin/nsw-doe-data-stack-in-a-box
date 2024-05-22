with source as (
    select *, from {{ source('raw', 'raw_google_analytics_user_metrics_date') }}
),

renamed as (
    select
        {{ adapter.quote("country") }},
        {{ adapter.quote("city") }},
        {{ adapter.quote("date") }},
        {{ adapter.quote("total_users_integer") }},
        {{ adapter.quote("new_users_integer") }},
        {{ adapter.quote("user_engagement_duration_seconds") }},
        {{ adapter.quote("_dlt_load_id") }},
        {{ adapter.quote("_dlt_id") }}

    from source
)

select *, from renamed
