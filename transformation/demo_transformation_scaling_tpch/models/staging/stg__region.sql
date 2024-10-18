with source as (
      select * from {{ source('tpch', 'region') }}
),
renamed as (
    select
        {{ adapter.quote("r_regionkey") }} as region_key,
        {{ adapter.quote("r_name") }} as region_name,
        {{ adapter.quote("r_comment") }} as region_comment

    from source
)
select * from renamed
