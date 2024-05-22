{{ simple_cte([
    ('stg__acara__student_numbers', 'stg__acara__student_numbers')
]) }},

prep as (
    select
        calendar_year,
        sex_gender,
        aboriginal_or_torres_strait_islander_status,
        Sum(student_count) as student_count,
    from stg__acara__student_numbers
    where
        1 = 1
        and state_territory = 'New South Wales'
        and school_sector = 'Government'
    group by all
),

final as (

    select

        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep.Calendar_Year', 'prep.Aboriginal_Or_Torres_Strait_Islander_Status', 'prep.Sex_Gender']) }}
            as _meta__fct__student__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions
        {# prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force  #}

        ----Local Dimensions
        prep.calendar_year,
        prep.sex_gender,
        prep.aboriginal_or_torres_strait_islander_status,

        Cast((prep.calendar_year || '-01-01') as date) as student_date,


        -- Measures
        prep.student_count,


    from prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
