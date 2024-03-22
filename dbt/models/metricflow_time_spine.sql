-- metricflow_time_spine.sql
-- by default, MetricFlow expects the timespine table to be named metricflow_time_spine and doesn't support using a different name.
with final as (
select * from {{ ref('dim_date') }}

)
select * from final