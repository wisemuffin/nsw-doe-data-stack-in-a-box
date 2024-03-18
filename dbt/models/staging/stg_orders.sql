with source as (
    select * from {{ source('raw','raw_orders_py') }}

),

renamed as (

    select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

    from source

)

select *,{{ add_audit_columns() }} from renamed
