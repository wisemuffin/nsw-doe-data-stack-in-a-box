---
title: Metric Tables
---

## Overview

<Alert status="info">
This data comes from a mix of New South Wales Department of Education and ACARA. This is a work in progress 🚧 data quality issues being investigated
</Alert>


## Metrics Consolidated Refference

### Summary
<DataTable data="{metrics_by_year_saved_query_latest}" search="true" />

### Detail by Year

<DataTable data="{metrics_by_year_saved_query}" search="true" />



```sql staff_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'staff_count'
```

```sql student_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'student_count'
```


```sql school_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'school_count'
```


```sql funding_aud_post_adjustments
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'funding_aud_post_adjustments'
```

```sql metrics_by_year_saved_query
select * from metrics_by_year_saved_query
```
```sql metrics_by_year_school_saved_query
from metrics_by_year_school_saved_query
```

```sql metrics_by_year_saved_query_latest
from metrics_by_year_saved_query_latest
```


```sql fct__web_analytics_monthly
WITH monthly_data AS (
    SELECT
        date_trunc('month', event_date) AS event_month,
        SUM(total_users) AS total_users
    FROM fct__web_analytics
    GROUP BY event_month

)
SELECT
    m.event_month,
    m.total_users,
    LAG(m.total_users) OVER (ORDER BY m.event_month ASC) as prior_month,
    COALESCE(m.total_users - LAG(m.total_users) OVER (ORDER BY m.event_month), 0) AS prior_month_growth,
    prior_month_growth / prior_month as prior_month_growth_pct
FROM monthly_data m
order by m.event_month desc
```
