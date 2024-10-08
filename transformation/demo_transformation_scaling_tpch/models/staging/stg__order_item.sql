with source as (
      select * from {{ source('main', 'lineitem') }}
),
renamed as (
    select
        {{ adapter.quote("l_orderkey") }} as order_key,
        {{ adapter.quote("l_partkey") }} as part_key,
        {{ adapter.quote("l_suppkey") }} as supplier_key,
        {{ adapter.quote("l_linenumber") }} as order_line_number,
        {{ adapter.quote("l_quantity") }} as quantity,
        {{ adapter.quote("l_extendedprice") }} as extended_price,
        {{ adapter.quote("l_discount") }} as discount_percentage,
        {{ adapter.quote("l_tax") }} as tax_rate,
        {{ adapter.quote("l_returnflag") }} as return_status_code,
        {{ adapter.quote("l_linestatus") }} as order_line_status_code,
        {{ adapter.quote("l_shipdate") }} as ship_date,
        {{ adapter.quote("l_commitdate") }} as commit_date,
        {{ adapter.quote("l_receiptdate") }} as receipt_date,
        {{ adapter.quote("l_shipinstruct") }} as ship_instruction,
        {{ adapter.quote("l_shipmode") }} as ship_mode_name,
        {{ adapter.quote("l_comment") }} as comment

    from source
)
select * from renamed
