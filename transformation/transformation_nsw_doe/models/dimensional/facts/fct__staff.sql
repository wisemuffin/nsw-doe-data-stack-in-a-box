{{ simple_cte([
    ('stg__acara__staff_numbers', 'stg__acara__staff_numbers')
]) }},
prep as (
    select Calendar_Year, 
        Staff_Function, 
        Sex_Gender, 
        FTE_Status, 
        Sum(Staff_Count) as Staff_Count
    from stg__acara__staff_numbers
    where 1=1
        and State_Territory = 'New South Wales'
        and School_Sector = 'Government'
    group by all
),

final AS (

    SELECT 
        
        --Primary Key
        {{dbt_utils.generate_surrogate_key(['prep.Calendar_Year', 'prep.Staff_Function', 'prep.Sex_Gender', 'prep.FTE_Status'])}} as _meta__fct__staff__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions
        {# prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force  #}

        ----Local Dimensions
        Calendar_Year, 
        Staff_Function, 
        Sex_Gender, 
        FTE_Status,
        
        (Calendar_Year || '-01-01')::date as staff_date,


        -- Measures
        Staff_Count


    FROM prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}

