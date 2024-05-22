{{ simple_cte([
    ('stg__acara__staff_numbers', 'stg__acara__staff_numbers')
]) }},

prep as (
    select
        calendar_year,
        staff_function,
        sex_gender,
        fte_status,
        Sum(staff_count) as staff_count,
    from stg__acara__staff_numbers
    where
        1 = 1
        and state_territory = 'New South Wales'
        and school_sector = 'Government'
    group by all
),

final as (

    select

        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep.Calendar_Year', 'prep.Staff_Function', 'prep.Sex_Gender', 'prep.FTE_Status']) }}
            as _meta__fct__staff__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions
        {# prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force  #}

        ----Local Dimensions
        prep.calendar_year,
        prep.staff_function,
        prep.sex_gender,
        prep.fte_status,

        Cast((prep.calendar_year || '-01-01') as date) as staff_date,


        -- Measures
        prep.staff_count,


    from prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
