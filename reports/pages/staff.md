# Staff

-- ```sql unique_items
-- select 
--     item
-- from needful_things.orders
-- group by 1
-- ```

<!-- <Dropdown
    name=selected_item
    data={unique_items}
    value=item
>
    <DropdownOption value="%" valueLabel="All Items"/>
</Dropdown> -->

-- ```sql orders_by_month
-- select
--     date_trunc('month', order_date) as month,
--     sum(sales) as sales_usd
-- from needful_things.orders
-- where item = '${inputs.selected_item.value}'
-- group by 1
-- ```

-- <BarChart
--     data={orders_by_month}
--     x=month
--     y=sales_usd
-- />