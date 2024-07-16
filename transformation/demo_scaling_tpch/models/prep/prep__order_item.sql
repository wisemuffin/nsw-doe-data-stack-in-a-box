{{
    config(
        materialized = 'table'
    )
}}
with orders as (

    select * from {{ ref('stg__order') }}

),

order_item as (

    select * from {{ ref('stg__order_item') }}

)

select

    orders.order_key,
    orders.order_date,
    orders.customer_key,
    orders.order_status_code,

    order_item.part_key,
    order_item.supplier_key,
    order_item.return_status_code,
    order_item.order_line_number,
    order_item.order_line_status_code,
    order_item.ship_date,
    order_item.commit_date,
    order_item.receipt_date,
    order_item.ship_mode_name,
    order_item.quantity,

    -- extended_price is actually the line item total,
    -- so we back out the extended price per item
    order_item.extended_price as gross_item_sales_amount,
    order_item.discount_percentage,
    order_item.tax_rate,

    (order_item.extended_price
        / nullif(order_item.quantity, 0)) as base_price,
    (base_price * (1 - order_item.discount_percentage))
         as discounted_price,

    (order_item.extended_price
        * (1 - order_item.discount_percentage))
    as discounted_item_sales_amount,
    -- We model discounts as negative amounts
    (-1 * order_item.extended_price
        * order_item.discount_percentage)
    as item_discount_amount,
    ((gross_item_sales_amount + item_discount_amount)
        * order_item.tax_rate) as item_tax_amount,
    (gross_item_sales_amount
        + item_discount_amount
        + item_tax_amount
    ) as net_item_sales_amount,

    {{ dbt_utils.generate_surrogate_key(['orders.order_key', 'order_item.order_line_number']) }} as order_item_key

from orders
join order_item
    on orders.order_key = order_item.order_key
order by
    orders.order_date
