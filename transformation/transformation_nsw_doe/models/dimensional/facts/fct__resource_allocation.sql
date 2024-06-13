{{ simple_cte([
    ('dim__school', 'dim__school'),
    ('prep__resource_allocation','prep__resource_allocation')
]) }},

final as (

    select
        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep__resource_allocation.School_Code','prep__resource_allocation.year']) }}
            as _meta__fct__resource_allocation__sk,

        --Natural Key
        {# prep__resource_allocation.School_Code || '|' || prep__resource_allocation.year as ram_school_code_by_year, #}

        prep__resource_allocation.school_code,
        prep__resource_allocation.year,

        --Foreign Keys
        ----Conformed Dimensions
        {{ get_keyed_nulls('dim__school._meta__dim__school__sk') }} as _meta__dim__school__sk,
        prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force

        ----Local Dimensions

        cast((prep__resource_allocation.year || '-01-01') as date)
            as resource_allocation_date,


        -- Measures
        prep__resource_allocation.original_ram_funding_aud
            as funding_aud_original,
        prep__resource_allocation.ram_funding_post_adjustments_aud
            as funding_aud_post_adjustments,


    from prep__resource_allocation
    left join
        dim__school
        on cast(prep__resource_allocation.school_code as varchar) = cast(dim__school.school_code as varchar)
    {# left join dim__date on prep__resource_allocation.year || '-01-01' = dim__date. #}
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
