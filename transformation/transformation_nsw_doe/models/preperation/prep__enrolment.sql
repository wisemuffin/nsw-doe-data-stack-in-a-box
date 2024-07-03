with unioned as (
    select
        central.school_performance_directorate,
        central.school_code,
        central.school_name,
        central.calendar_year,
        central.enrolments_central as enrolments,
        'central' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_central') }} as central
    union all
    select
        prim.school_performance_directorate,
        prim.school_code,
        prim.school_name,
        prim.calendar_year,
        prim.enrolments_primary as enrolments,
        'primary' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_primary') }} as prim
    union all
    select
        secondary.school_performance_directorate,
        secondary.school_code,
        secondary.school_name,
        secondary.calendar_year,
        secondary.enrolments_secondary as enrolments,
        'secondary' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_secondary') }} as secondary
    union all
    select
        ssp.school_performance_directorate,
        ssp.school_code,
        ssp.school_name,
        ssp.calendar_year,
        ssp.enrolments_ssp as enrolments,
        'ssp' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_ssp') }} as ssp
),

final as (
    select
        unioned.school_performance_directorate,
        unioned.school_code,
        unioned.school_name,
        unioned.calendar_year,
        unioned.enrolments,
    from unioned
    where unioned.school_code != '-' -- data quality issue
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
