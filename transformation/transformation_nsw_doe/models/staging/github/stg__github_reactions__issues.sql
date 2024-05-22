with source as (
    select *, from {{ source('raw', 'raw_github_reactions_issues') }}
),

renamed as (
    select
        {{ adapter.quote("number") }},
        {{ adapter.quote("url") }},
        {{ adapter.quote("title") }},
        {{ adapter.quote("body") }},
        {{ adapter.quote("author__login") }},
        {{ adapter.quote("author__avatar_url") }},
        {{ adapter.quote("author__url") }},
        {{ adapter.quote("author_association") }},
        {{ adapter.quote("closed") }},
        {{ adapter.quote("created_at") }},
        {{ adapter.quote("state") }},
        {{ adapter.quote("updated_at") }},
        {{ adapter.quote("reactions_total_count") }},
        {{ adapter.quote("comments_total_count") }},
        {{ adapter.quote("_dlt_load_id") }},
        {{ adapter.quote("_dlt_id") }},
        {{ adapter.quote("closed_at") }}

    from source
)

select *, from renamed
