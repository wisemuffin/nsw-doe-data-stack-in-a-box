{{
    config(
        materialized = 'table'
    )
}}
with orders_items as (

    select * from {{ ref('prep__order_item') }}

),

parts_suppliers as (

    select * from {{ ref('stg__part_supplier') }}

),

final as (
    select

        orders_items.order_item_key,
        orders_items.order_key,
        orders_items.order_date,
        orders_items.customer_key,
        orders_items.order_status_code,

        orders_items.part_key,
        orders_items.supplier_key,
        orders_items.return_status_code,
        orders_items.order_line_number,
        orders_items.order_line_status_code,
        orders_items.ship_date,
        orders_items.commit_date,
        orders_items.receipt_date,
        orders_items.ship_mode_name,
        parts_suppliers.supplier_cost_amount,
        {# parts_suppliers.retail_price, #}
        orders_items.base_price,
        orders_items.discount_percentage,
        orders_items.discounted_price,
        orders_items.tax_rate,

        1 as order_item_count,
        orders_items.quantity,

        orders_items.gross_item_sales_amount,
        orders_items.discounted_item_sales_amount,
        orders_items.item_discount_amount,
        orders_items.item_tax_amount,
        orders_items.net_item_sales_amount

    from orders_items
    join parts_suppliers
        on orders_items.part_key = parts_suppliers.part_key
            and orders_items.supplier_key = parts_suppliers.supplier_key
)
select
    final.*
from
    final
order by
    final.order_date
