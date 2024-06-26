{{ config(
    post_hook=[
      "{{ missing_member_column(primary_key = '_meta__dim__school__sk', not_null_test_cols = []) }}"
    ]
) }}



with final as (

    select
        --Surrogate Key
        {{ dbt_utils.generate_surrogate_key(['ece_centre_id']) }}
            as _meta__dim__school__sk,


        --Natural Key
        ece_centre_id,

        --School Information
        location_id,
        type_of_provider,
        provider_name,
        address,
        suburb,
        state,
        postcode,
        latitude,
        longitude,
        geo_data,

    from {{ ref('stg__nsw_doe_datansw__early_childhood_education_centres') }}

)

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveg",
    updated_by="@daveg",
    created_date="2024-06-22",
    updated_date="2024-06-22"
) }}
