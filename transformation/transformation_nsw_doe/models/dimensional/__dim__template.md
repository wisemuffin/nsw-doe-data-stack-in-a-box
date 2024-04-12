```sql
{{ config({
    "post-hook": "{{ missing_member_column(primary_key = 'dim_crm_person_id') }}"
    })
}}

--Surrogate Key
_sk
--Natural Key
_nk


select {{dbt_utils.dbt_utils.generate_surrogate_key('-1')}}

{{ dbt_audit(
    cte_ref="final",
    created_by="@daveyg",
    updated_by="@daveyg",
    created_date="2023-08-22",
    updated_date="2023-08-29"
) }}
```