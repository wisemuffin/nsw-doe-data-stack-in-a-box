```sql
{{ simple_cte([
    ('prep_crm_person', 'prep_crm_person'),
    ('sfdc_lead_source','sfdc_lead_source')
    ]) }}


--Primary Key

fct_template_sk

--Foreign Keys
----Conformed Dimensions
get_keyed_nulls(dim_template_sk) as dim_template_sk

----Local Dimensions


-- Dates




{{ dbt_audit(
    cte_ref="final",
    created_by="@daveyg",
    updated_by="@daveyg",
    created_date="2023-08-22",
    updated_date="2023-08-29"
) }}
```