{{
  config(
    materialized = 'table',
    )
}}
with 

dim_date as (
    
    --for BQ adapters use "DATE('01/01/2000','mm/dd/yyyy')"

    {{dbt_date.get_date_dimension('2023-01-01', '2027-12-31')}}


)



select * from dim_date