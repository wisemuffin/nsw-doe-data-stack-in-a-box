with source as (
    select *, from {{ source('raw', 'raw__nsw_doe_datansw__ram') }}
),

renamed as (
    select
        {{ adapter.quote("School Code") }} as school_code,
        {{ adapter.quote("School Full Name") }} as school_full_name,
        {{ adapter.quote("year") }},
        TRY_CAST(REPLACE(REPLACE({{ adapter.quote("RAM Funding - post Adjustments $") }}, '$', ''), ',', '') as INTEGER) as ram_funding_post_adjustments_aud,
        TRY_CAST(
            REPLACE(
                REPLACE(
                    {{ adapter.quote("Original RAM Funding $ ") }}, '$', ''
                ),
                ',',
                ''
            ) as INTEGER
        ) as original_ram_funding_aud,
        TRY_CAST(
            REPLACE(
                REPLACE(
                    {{ adapter.quote("Sum of RAM Funding (incl oncosts) $") }},
                    '$',
                    ''
                ),
                ',',
                ''
            ) as INTEGER
        ) as sum_of_ram_funding_incl_oncosts_aud,
        TRY_CAST(
            REPLACE(
                REPLACE(
                    {{ adapter.quote(" Sum of RAM Funding (incl oncosts) $ ") }},
                    '$',
                    ''
                ),
                ',',
                ''
            ) as INTEGER
        ) as _sum_of_ram_funding_incl_oncosts_aud,
        {{ adapter.quote("_load_timestamp") }} as _meta__load_source_timestamp,
        {{ adapter.quote("_source") }}

    from source
),

final as (
    select *,
    from renamed
)

  {{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
