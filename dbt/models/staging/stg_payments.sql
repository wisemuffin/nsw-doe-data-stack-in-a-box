with source as (
      select * from {{ source('raw', 'raw_payments_py') }}
),
renamed as (
    select
        {{ adapter.quote("id") }},
        {{ adapter.quote("order_id") }},
        {{ adapter.quote("payment_method") }},
        {{ adapter.quote("amount") }} / 100 as "amount" -- amount stored as centrs so convert to dollars

    from source
)
select *,{{ add_audit_columns() }} from renamed
  
  