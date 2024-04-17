{{ simple_cte([
    ('dim__school', 'dim__school'),
    ('prep__school','prep__school')
]) }},

final AS (

    SELECT 
        --Primary Key
        {{dbt_utils.generate_surrogate_key(['prep__school.School_Code'])}} as _meta__fct__school__sk,

        --Natural Key
        prep__school.School_Code,

        --Foreign Keys
        ----Conformed Dimensions
        {{ get_keyed_nulls('dim__school._meta__dim__school__sk') }} as _meta__dim__school__sk,

        _meta__load_source_timestamp as school_date,

        ----Local Dimensions

        -- Measures
        1 as school_cnt


    FROM prep__school
    left join dim__school on prep__school.School_Code = dim__school.School_Code
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
