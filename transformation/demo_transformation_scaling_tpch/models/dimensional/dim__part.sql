with parts as (

    select * from {{ ref('stg__part') }}

),

final as (

    select
        parts.part_key,
        parts.part_name,
        parts.part_manufacturer_name,
        parts.part_brand_name,
        parts.part_type_name,
        parts.part_size,
        parts.part_container_desc,
        parts.retail_price
    from parts
)

select
    final.*
from
    final
order by
    final.part_key
