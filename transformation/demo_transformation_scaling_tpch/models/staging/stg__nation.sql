with source as (
      select * from {{ source('tpch', 'nation') }}
),
renamed as (
    select
        {{ adapter.quote("n_nationkey") }} as nation_key,
        {{ adapter.quote("n_name") }} as nation_name,
        {{ adapter.quote("n_regionkey") }} as region_key,
        {{ adapter.quote("n_comment") }} as nation_comment

    from source
)
select * from renamed
