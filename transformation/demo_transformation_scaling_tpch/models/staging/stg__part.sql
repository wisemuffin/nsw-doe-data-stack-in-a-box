with source as (
      select * from {{ source('tpch', 'part') }}
),
renamed as (
    select
        {{ adapter.quote("p_partkey") }} as part_key,
        {{ adapter.quote("p_name") }} as part_name,
        {{ adapter.quote("p_mfgr") }} as part_manufacturer_name,
        {{ adapter.quote("p_brand") }} as part_brand_name,
        {{ adapter.quote("p_type") }} as part_type_name,
        {{ adapter.quote("p_size") }} as part_size,
        {{ adapter.quote("p_container") }} as part_container_desc,
        {{ adapter.quote("p_retailprice") }} as retail_price,
        {{ adapter.quote("p_comment") }} as part_comment

    from source
)
select * from renamed
