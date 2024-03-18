with source as (

    select * from {{ source('raw','raw_customers_py') }}

),

renamed as (

    select
        id as customer_id,
        first_name,
        last_name

    from source

)

select *,{{ add_audit_columns() }} from renamed
