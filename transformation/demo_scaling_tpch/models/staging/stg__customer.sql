with source as (
      select * from {{ source('main', 'customer') }}
),
renamed as (
    select
        {{ adapter.quote("c_custkey") }} as customer_key,
        {{ adapter.quote("c_name") }} as customer_name,
        {{ adapter.quote("c_address") }} as customer_address,
        {{ adapter.quote("c_nationkey") }} as nation_key,
        {{ adapter.quote("c_phone") }} as customer_phone_number,
        {{ adapter.quote("c_acctbal") }} as customer_account_balance,
        {{ adapter.quote("c_mktsegment") }} as customer_market_segment_name,
        {{ adapter.quote("c_comment") }} as customer_comment

    from source
)
select * from renamed
