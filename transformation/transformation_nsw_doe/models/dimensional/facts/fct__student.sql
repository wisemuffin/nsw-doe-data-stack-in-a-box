{{ simple_cte([
    ('stg__acara__student_numbers', 'stg__acara__student_numbers')
]) }},
prep as (
    select Calendar_Year, 
        Sex_Gender,
        Aboriginal_Or_Torres_Strait_Islander_Status, 
        Sum(Student_Count) as Student_Count 
    from stg__acara__student_numbers
    where 1=1
        and State_Territory = 'New South Wales'
        and School_Sector = 'Government'
        and Full_Time_Part_Time_Status = 'All'
    group by all
),

final AS (

    SELECT 
        
        --Primary Key
        {{dbt_utils.generate_surrogate_key(['prep.Calendar_Year', 'prep.Aboriginal_Or_Torres_Strait_Islander_Status', 'prep.Sex_Gender'])}} as _meta__fct__student__sk,

        --Natural Key

        --Foreign Keys
        ----Conformed Dimensions
        {# prep__resource_allocation.year || '-01-01' as _meta__dim__date__sk, -- dont love this. 🚧 TODO - if only one date in fact this works...also doesnt force  #}

        ----Local Dimensions
        Calendar_Year, 
        Sex_Gender, 
        Aboriginal_Or_Torres_Strait_Islander_Status,
        
        (Calendar_Year || '-01-01')::date as student_date,


        -- Measures
        Student_Count


    FROM prep
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}

