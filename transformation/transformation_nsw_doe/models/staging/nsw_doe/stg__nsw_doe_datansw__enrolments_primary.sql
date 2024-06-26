with source as (
    select *, from {{ source('raw', 'raw_nsw_doe_datansw_enrolments_primary') }}
),

renamed as (
    select
        {{ adapter.quote("school_performance_directorate") }},
        {{ adapter.quote("school_code") }},
        {{ adapter.quote("school_name") }},
        {{ adapter.quote("_2020") }},
        {{ adapter.quote("_2021") }},
        {{ adapter.quote("_2022") }},
        {{ adapter.quote("_2023") }},
        {{ adapter.quote("_2024") }},
    {# {{ adapter.quote("_dlt_load_id") }}, #}
    {# {{ adapter.quote("_dlt_id") }} #}

    from source
),

unpivoted as (
    unpivot renamed
    on columns(* exclude (school_performance_directorate, school_code, school_name))
    into
    name year
    value enrolments_primary
),

final as (
    select
        school_performance_directorate,
        school_code,
        school_name,
        cast(substring(year, 2, 4) as INTEGER) as calendar_year,
        cast(enrolments_primary as DECIMAL) as enrolments_primary,
    from unpivoted
)

  {{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
