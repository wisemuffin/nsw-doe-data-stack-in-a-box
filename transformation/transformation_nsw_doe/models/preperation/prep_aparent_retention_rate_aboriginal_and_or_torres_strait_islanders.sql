with stg__nsw_doe_datahub__aparent_retention_rate_aboriginal_and_or_torres_strait_islanders as (
    from {{ ref('stg__nsw_doe_datahub__aparent_retention_rate_aboriginal_and_or_torres_strait_islanders') }}
),

pivoted as (
    pivot stg__nsw_doe_datahub__aparent_retention_rate_aboriginal_and_or_torres_strait_islanders
    on retention_period
    using sum(aparent_retention_rate_aboriginal_and_or_torres_strait_islanders)
    {# GROUP BY ⟨calendar_year⟩ #}
    {# ORDER BY ⟨calendar_year⟩ #}
),

final as (
    select
        calendar_year,
        "Year 10 to 12" as aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders,
        "Year 7 to 10" as aparent_retention_rate_7_to_10_aboriginal_and_or_torres_strait_islanders,
        "Year 7 to 12" as aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders,
    from pivoted
)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-04-06",
    updated_date="2024-04-06"
) }}
