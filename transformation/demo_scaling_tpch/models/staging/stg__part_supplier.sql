with source as (
      select * from {{ source('main', 'partsupp') }}
),
renamed as (
    select
        {{ adapter.quote("ps_partkey") }} as part_key,
        {{ adapter.quote("ps_suppkey") }} as supplier_key,
        {{ adapter.quote("ps_availqty") }} as available_quantaty,
        {{ adapter.quote("ps_supplycost") }} as supplier_cost_amount,
        {{ adapter.quote("ps_comment") }} as comment

    from source
)
select * from renamed
