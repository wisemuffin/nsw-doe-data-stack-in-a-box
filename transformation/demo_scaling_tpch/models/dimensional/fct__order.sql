{{
    config(
        materialized = 'incremental',
        unique_key = 'order_key',
        on_schema_change = 'sync_all_columns'

    )
}}
with orders as (

    select * from {{ ref('stg__order') }}

    {% if is_incremental() %}

    -- this filter will only be applied on an incremental run
    where order_date > (select max(order_date) from {{ this }})

    {% endif %}

),

orders_items as (

    select * from {{ ref('prep__order_item') }}

    {% if is_incremental() %}

    -- this filter will only be applied on an incremental run
    where order_date > (select max(order_date) from {{ this }})

    {% endif %}

),

order_item_summary as (

    select
        orders_items.order_key,
        sum(orders_items.gross_item_sales_amount) as gross_item_sales_amount,
        sum(orders_items.item_discount_amount) as item_discount_amount,
        sum(orders_items.item_tax_amount) as item_tax_amount,
        sum(orders_items.net_item_sales_amount) as net_item_sales_amount
    from orders_items
    group by orders_items.order_key
),
final as (

    select

        orders.order_key,
        orders.order_date,
        orders.customer_key,
        orders.order_status_code,
        orders.order_priority_code,
        orders.order_clerk_name,
        orders.shipping_priority,
        1 as order_count,
        'order status: '|| orders.order_status_code ||' - sales amount: '||order_item_summary.net_item_sales_amount as item_summary,
        order_item_summary.gross_item_sales_amount - order_item_summary.item_discount_amount - order_item_summary.item_tax_amount as net_check_amount,
        order_item_summary.gross_item_sales_amount,
        order_item_summary.item_discount_amount,
        order_item_summary.item_tax_amount,
        order_item_summary.net_item_sales_amount
    from orders
    join order_item_summary
        on orders.order_key = order_item_summary.order_key
)
select *
from final
{# {{ dbt_audit(
    cte_ref="final",
    created_by="@davidgriffiths",
    updated_by="@wisemuffin",
    created_date="2024-07-06",
    updated_date="2024-07-06"
) }} #}
