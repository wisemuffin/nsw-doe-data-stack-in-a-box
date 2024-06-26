with source as (
    select *, from {{ source('raw', 'raw__nsw_doe_datansw__attendance') }}
),

renamed as (
    select
        {{ adapter.quote("school_code") }},
        {{ adapter.quote("school_name") }},
        {{ adapter.quote("2011") }},
        {{ adapter.quote("2012") }},
        {{ adapter.quote("2013") }},
        {{ adapter.quote("2014") }},
        {{ adapter.quote("2015") }},
        {{ adapter.quote("2016") }},
        {{ adapter.quote("2017") }},
        {{ adapter.quote("2018") }},
        {{ adapter.quote("2019") }},
        {{ adapter.quote("2021") }},
        {{ adapter.quote("2022") }},
        {{ adapter.quote("2023") }},
    {# {{ adapter.quote("_load_timestamp") }}, #}
    {# {{ adapter.quote("_source") }} #}

    from source
),

unpivoted as (
    unpivot renamed
    on columns(* exclude (school_code, school_name))
    into
    name year
    value attendance
),

final as (
    select
        school_code,
        school_name,
        cast(substring(year, 1, 4) as INTEGER) as calendar_year,
        cast(replace(attendance, ',', '') as DECIMAL) as attendance,
    from unpivoted
    where attendance not in ('na', 'sp')
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-20",
    updated_date="2024-06-20"
) }}
