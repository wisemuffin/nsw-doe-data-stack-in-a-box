with source as (
      select * from {{ source('raw', 'raw_payments_py') }}
),
renamed as (
    select
        {{ adapter.quote("id") }},
        {{ adapter.quote("order_id") }},
        {{ adapter.quote("payment_method") }},
        {{ adapter.quote("amount") }},
        {{ adapter.quote("_load_timestamp") }},
        {{ adapter.quote("_source") }}

    from source
)
select * from renamed
  