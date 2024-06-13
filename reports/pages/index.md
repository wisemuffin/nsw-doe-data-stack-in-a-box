---
title: NSW Public Schools
---

## Overview

<Alert status="info">
This data comes from a mix of New South Wales Department of Education and ACARA. This is a work in progress 🚧 data quality issues being investigated
</Alert>

<Alert status="warning">
Warning for Developer: Visuals update when sql in evidence is changed. But source cache doesnt get notified when data changes in database. 🚧 Figure out longer term fix.
</Alert>

<BigValue
    data={staff_count}
    title="Staff"
    value="metric_value__latest_year"
    fmt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  />
<LinkButton  url='/staff'>
  More Details on Staff
</LinkButton >


<LineBreak/>

<BigValue
    data={student_count}
    title="Students"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  />
<LinkButton  url='/student'>
  More Details on students
</LinkButton >
<LineBreak/>

<BigValue
    data={school_count}
    title="Schools"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  />
<LinkButton  url='/school'>
  More Details on schools
</LinkButton >
<LineBreak/>

<BigValue
    data={funding_aud_post_adjustments}
    title="Funding"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  />
<LinkButton  url='/funding'>
  More Details on funding
</LinkButton >
<LineBreak/>



<BigValue
  data={fct__web_analytics_monthly}
  value=total_users
  title="Visualisation Users"
  sparkline=event_month
  comparison=prior_month_growth_pct
  comparisonFmt=pct1
  comparisonTitle="vs. Last Month"
/>

<LinkButton  url='/useage'>
  More Details on useage
</LinkButton >
<LineBreak/>


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
