{{ config(
    post_hook=[
      "{{ missing_member_column(primary_key = '_meta__dim__school__sk', not_null_test_cols = []) }}"
    ]
) }}



with final as (

    select
        --Surrogate Key
        {{ dbt_utils.generate_surrogate_key(['university_campus_name']) }}
            as _meta__dim__school__sk,


        --Natural Key

        --uni Information
        university_name,
        university_campus_name,
        address,
        street,
        suburb,
        state,
        postcode,
        latitude,
        longitude,
        geo_data,

    from {{ ref('stg__nsw_doe_datansw_university') }}

)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
