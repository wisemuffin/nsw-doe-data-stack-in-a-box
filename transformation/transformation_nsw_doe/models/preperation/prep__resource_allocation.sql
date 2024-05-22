with final as (
    select
        year,
        school_code::int as school_code,
        coalesce(
            original_ram_funding_aud,
            sum_of_ram_funding_incl_oncosts_aud,
            _sum_of_ram_funding_incl_oncosts_aud
        )::integer as original_ram_funding_aud,
        coalesce(
            ram_funding_post_adjustments_aud,
            sum_of_ram_funding_incl_oncosts_aud,
            _sum_of_ram_funding_incl_oncosts_aud
        )::integer as ram_funding_post_adjustments_aud,

    from {{ ref("stg__nsw_doe_datahub__ram") }}
    where school_code not like '%Total%' -- files contain totals 💩
)


{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
{# 
-- figuring out RAM mapping, confusing huh? - part 1
select year, 
    sum("Original_RAM_Funding_AUD") as "Original_RAM_Funding_AUD",
    sum("RAM_Funding_post_Adjustments_AUD") as "RAM_Funding_post_Adjustments_AUD",
    sum("Original_RAM_Funding_AUD_1") as "Original_RAM_Funding_AUD_1",
    sum("Sum_of_RAM_Funding_incl_oncosts_AUD") as "Sum_of_RAM_Funding_incl_oncosts_AUD",
    sum("_Sum_of_RAM_Funding_incl_oncosts_AUD") as "_Sum_of_RAM_Funding_incl_oncosts_AUD"
from {{ ref("stg__nsw_doe_datahub__ram") }}
group by all
order by all

-- example of 
with temp as (
select year,
    -- assuming no adjustments for 2020 and 2019
    coalesce(Original_RAM_Funding_AUD, Original_RAM_Funding_AUD_1, Sum_of_RAM_Funding_incl_oncosts_AUD,_Sum_of_RAM_Funding_incl_oncosts_AUD) as Original_RAM_Funding_AUD,
    coalesce(RAM_Funding_post_Adjustments_AUD, Sum_of_RAM_Funding_incl_oncosts_AUD,_Sum_of_RAM_Funding_incl_oncosts_AUD) as RAM_Funding_post_Adjustments_AUD
from {{ ref("stg__nsw_doe_datahub__ram") }}
)
select year, 
    sum("Original_RAM_Funding_AUD") as "Original_RAM_Funding_AUD",
    sum("RAM_Funding_post_Adjustments_AUD") as "RAM_Funding_post_Adjustments_AUD"
from temp
group by all
order by all 
#}