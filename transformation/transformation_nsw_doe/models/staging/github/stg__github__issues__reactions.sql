with source as (
      select * from {{ source('raw_github', 'issues__reactions') }}
),
renamed as (
    select
        {{ adapter.quote("user__login") }},
        {{ adapter.quote("user__avatar_url") }},
        {{ adapter.quote("user__url") }},
        {{ adapter.quote("content") }},
        {{ adapter.quote("created_at") }},
        {{ adapter.quote("_dlt_parent_id") }},
        {{ adapter.quote("_dlt_list_idx") }},
        {{ adapter.quote("_dlt_id") }}

    from source
)
select * from renamed
  