with unioned as (
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_central as enrolments,
        'central' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_central') }}
    union all
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_primary as enrolments,
        'primary' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_primary') }}
    union all
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_secondary as enrolments,
        'secondary' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_secondary') }}
    union all
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_ssp as enrolments,
        'ssp' as school_type,
    from {{ ref('stg__nsw_doe_datansw__enrolments_ssp') }}
)
, final as (
    from unioned
    where school_code != '-' -- data quality issue
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
