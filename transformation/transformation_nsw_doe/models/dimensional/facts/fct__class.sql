with stg__nsw_doe_datansw__class_size as (
    from {{ ref('stg__nsw_doe_datansw__class_size') }}
),
{# , dim__school as (
    from {{ ref('dim__school') }}
) #}
final as (

    select
        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['stg__nsw_doe_datansw__class_size.calendar_year']) }}
            as _meta__fct__school__sk,

        --Natural Key
        {# stg__nsw_doe_datansw__class_size.calendar_year, #}

        --Foreign Keys
        ----Conformed Dimensions
        {# {{ get_keyed_nulls('dim__school._meta__dim__school__sk') }} as _meta__dim__school__sk, #}


        ----Local Dimensions
        stg__nsw_doe_datansw__class_size.calendar_year,
        cast((stg__nsw_doe_datansw__class_size.calendar_year || '-01-01') as date) as calendar_date, -- this is ugly 🚧 TODO, required for dbt metrics layer


        -- Measures
        stg__nsw_doe_datansw__class_size.k as average_class_size_k,
        stg__nsw_doe_datansw__class_size.year_1 as average_class_size_year_1,
        stg__nsw_doe_datansw__class_size.year_2 as average_class_size_year_2,
        stg__nsw_doe_datansw__class_size.year_3 as average_class_size_year_3,
        stg__nsw_doe_datansw__class_size.year_4 as average_class_size_year_4,
        stg__nsw_doe_datansw__class_size.year_5 as average_class_size_year_5,
        stg__nsw_doe_datansw__class_size.year_6 as average_class_size_year_6,
        stg__nsw_doe_datansw__class_size.k_6 as average_class_size_k_6,


    from stg__nsw_doe_datansw__class_size
    {# left join dim__school on stg__nsw_doe_datansw__class_size.school_code = dim__school.school_code #}
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
