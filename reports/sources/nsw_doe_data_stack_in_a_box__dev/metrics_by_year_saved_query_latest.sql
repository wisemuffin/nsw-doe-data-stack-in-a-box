-- apply window logic to get latest value
with prep as (
    UNPIVOT analytics.metrics_by_year_saved_query
    ON * EXCLUDE (metric_time__year)
    INTO
        NAME metric_name
        VALUE metric_value
),
prep_rank_period as (
    select *,
        row_number() OVER (PARTITION BY "metric_name" ORDER  BY "metric_time__year" desc) AS "period_rank"
    from prep
),
latest_year as (
    select metric_name, 
        metric_value as metric_value__latest_year, 
        year(metric_time__year) as metric_time__year__latest_year,
    from prep_rank_period where period_rank=1
),
prior_year as (
    select metric_name, 
        metric_value as metric_value__prior_year, 
        year(metric_time__year) as metric_time__year__prior_year
    from prep_rank_period where period_rank=2
),
final as (
    select latest_year.metric_name, 
        latest_year.metric_value__latest_year, 
        prior_year.metric_value__prior_year, 
        latest_year.metric_time__year__latest_year,
        prior_year.metric_time__year__prior_year,
        latest_year.metric_value__latest_year / prior_year.metric_value__prior_year - 1 as metric_value__comp
    from latest_year
    left join prior_year on latest_year.metric_name = prior_year.metric_name
)
select * from final