with source as (
      select * from {{ source('main', 'supplier') }}
),
renamed as (
    select
        {{ adapter.quote("s_suppkey") }} as supplier_key,
        {{ adapter.quote("s_name") }} as supplier_name,
        {{ adapter.quote("s_address") }} as supplier_address,
        {{ adapter.quote("s_nationkey") }} as nation_key,
        {{ adapter.quote("s_phone") }} as supplier_phone_number,
        {{ adapter.quote("s_acctbal") }} as supplier_account_balance,
        {{ adapter.quote("s_comment") }} as supplier_comment

    from source
)
select * from renamed
