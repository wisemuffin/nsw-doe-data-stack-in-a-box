with stg__nsw_doe_datansw__attendance as (
    from {{ ref('stg__nsw_doe_datansw__attendance') }}
),

dim__school as (
    from {{ ref('dim__school') }}
),

final as (

    select
        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['stg__nsw_doe_datansw__attendance.school_code', 'stg__nsw_doe_datansw__attendance.calendar_year']) }}
            as _meta__fct__school__sk,

        --Natural Key
        stg__nsw_doe_datansw__attendance.school_code,

        --Foreign Keys
        ----Conformed Dimensions
        dim__school._meta__dim__school__sk,


        ----Local Dimensions
        stg__nsw_doe_datansw__attendance.calendar_year,
        cast((stg__nsw_doe_datansw__attendance.calendar_year || '-01-01') as date) as calendar_date, -- this is ugly 🚧 TODO, required for dbt metrics layer


        -- Measures
        stg__nsw_doe_datansw__attendance.attendance /100  as attendance,


    from stg__nsw_doe_datansw__attendance
    left join dim__school on stg__nsw_doe_datansw__attendance.school_code = dim__school.school_code
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-06",
    updated_date="2024-06-06"
) }}
