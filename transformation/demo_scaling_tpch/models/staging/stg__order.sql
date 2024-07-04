with source as (
      select * from {{ source('main', 'orders') }}
),
renamed as (
    select
        {{ adapter.quote("o_orderkey") }} as order_key,
        {{ adapter.quote("o_custkey") }} as customer_key,
        {{ adapter.quote("o_orderstatus") }} as order_status_code,
        {{ adapter.quote("o_totalprice") }} as total_price,
        {{ adapter.quote("o_orderdate") }} as order_date,
        {{ adapter.quote("o_orderpriority") }} as order_priority_code,
        {{ adapter.quote("o_clerk") }} as order_clerk_name,
        {{ adapter.quote("o_shippriority") }} as shipping_priority,
        {{ adapter.quote("o_comment") }} as order_comment

    from source
)
select * from renamed
