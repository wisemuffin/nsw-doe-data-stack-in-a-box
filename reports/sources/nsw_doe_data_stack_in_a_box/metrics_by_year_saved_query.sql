
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
final as (
    select
        prep_rank_period.metric_name,
        prep_rank_period.metric_value,
        prep_rank_period_lagged_1_year.metric_value metric_value__prior_year,
        prep_rank_period.metric_time__year,
        prep_rank_period_lagged_1_year.metric_time__year as metric_time__year__prior_year,
        prep_rank_period.metric_value / prep_rank_period_lagged_1_year.metric_value - 1 as metric_value__comp
    from prep_rank_period
    left join prep_rank_period as prep_rank_period_lagged_1_year on prep_rank_period.metric_name = prep_rank_period_lagged_1_year.metric_name and prep_rank_period.metric_time__year = date_add(prep_rank_period_lagged_1_year.metric_time__year, INTERVAL 1 YEAR)
)
select * from final

order by metric_time__year desc
