with customers as (

    select * from {{ ref('stg__customer') }}

),

nations as (

    select * from {{ ref('stg__nation') }}
),

regions as (

    select * from {{ ref('stg__region') }}

),

final as (
    select
        customers.customer_key,
        customers.customer_name,
        customers.customer_address,
        {# nations.nation_key as customer_nation_key, #}
        nations.nation_name as customer_nation_name,
        {# regions.region_key as customer_region_key, #}
        regions.region_name as customer_region_name,
        customers.customer_phone_number,
        customers.customer_account_balance,
        customers.customer_market_segment_name
    from customers
    join nations
        on customers.nation_key = nations.nation_key
    join regions
        on nations.region_key = regions.region_key
)

select
    final.*
from
    final
order by
    final.customer_key
