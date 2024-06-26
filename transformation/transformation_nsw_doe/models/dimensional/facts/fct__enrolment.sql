with prep__enrolment as (
    from {{ ref('prep__enrolment') }}
),

dim__school as (
    from {{ ref('dim__school') }}
),

final as (

    select
        --Primary Key
        {{ dbt_utils.generate_surrogate_key(['prep__enrolment.school_code', 'prep__enrolment.calendar_year']) }}
            as _meta__fct__school__sk,

        --Natural Key
        prep__enrolment.school_code,

        --Foreign Keys
        ----Conformed Dimensions
        dim__school._meta__dim__school__sk,


        ----Local Dimensions
        prep__enrolment.calendar_year,
        cast((prep__enrolment.calendar_year || '-01-01') as date) as calendar_date, -- this is ugly 🚧 TODO, required for dbt metrics layer


        -- Measures
        prep__enrolment.enrolments,


    from prep__enrolment
    left join dim__school on prep__enrolment.school_code = dim__school.school_code
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
