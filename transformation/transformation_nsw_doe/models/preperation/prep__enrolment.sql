with final as (
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_central as enrolments,
        'central' as school_type,
    from {{ ref('stg__nsw_doe_datahub__enrolments_central') }}
    union all
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_primary as enrolments,
        'primary' as school_type,
    from {{ ref('stg__nsw_doe_datahub__enrolments_primary') }}
    union all
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_secondary as enrolments,
        'secondary' as school_type,
    from {{ ref('stg__nsw_doe_datahub__enrolments_secondary') }}
    union all
    select
        school_performance_directorate,
        school_code,
        school_name,
        calendar_year,
        enrolments_ssp as enrolments,
        'ssp' as school_type,
    from {{ ref('stg__nsw_doe_datahub__enrolments_ssp') }}
)


{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
