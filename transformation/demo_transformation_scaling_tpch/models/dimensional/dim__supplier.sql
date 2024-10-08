with suppliers as (

    select * from {{ ref('stg__supplier') }}

),

nations as (

    select * from {{ ref('stg__nation') }}
),

regions as (

    select * from {{ ref('stg__region') }}

),

final as (

    select
        suppliers.supplier_key,
        suppliers.supplier_name,
        suppliers.supplier_address,
        nations.nation_key as supplier_nation_key,
        nations.nation_name as supplier_nation_name,
        regions.region_key as supplier_region_key,
        regions.region_name as supplier_region_name,
        suppliers.supplier_phone_number,
        suppliers.supplier_account_balance
    from suppliers
    join nations
        on suppliers.nation_key = nations.nation_key
    join regions
        on nations.region_key = regions.region_key
)

select
    final.*
from
    final
order by
    final.supplier_key
