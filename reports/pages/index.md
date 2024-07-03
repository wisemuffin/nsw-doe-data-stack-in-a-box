---
title: New South Wales Public School
---


<Alert status="info">

ℹ️ This Data Visualisation is powered by [nsw-doe-data-stack-in-a-box](https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box). With the push of one button you can have your own data stack!

<LineBreak/>

The data comes from a mix of [New South Wales Department of Education](https://education.nsw.gov.au/) via [Data.NSW](https://data.nsw.gov.au/) and [ACARA](https://acara.edu.au/).

</Alert>

<Alert status="warning">
⚠️ Warning this data is being validated. Do not use.
</Alert>


## Overview


<!-- <BigValue
    data={attendance_rate}
    title="Attendance"
    value="metric_value__latest_year"
    fmt="0.0%"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={attendance_rate}
    title="Attendance"
    value="metric_value"
    fmt="0.0%"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={attendance_rate_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>
<Alert status="warning">
⚠️ Attendance metric is averaging an average (which statistically is a terrible idea). Do not use. Only indicative.
</Alert>
<LineBreak/>
<!-- <BigValue
    data={aparent_retention_rate_7_to_10}
    title="Aparent retention rate 7 to 10"
    value="metric_value__latest_year"
    fmt="0.0%"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={aparent_retention_rate_7_to_10}
    title="Aparent retention rate 7 to 10"
    value="metric_value"
    fmt="0.0%"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={aparent_retention_rate_7_to_10_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>

  <!-- <BigValue
    data={aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders}
    title="Aparent retention rate 7 to 12 (Aboriginal and or Torres Strait Islanders)"
    value="metric_value__latest_year"
    fmt="0.0%"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders}
    title="Aparent retention rate 7 to 12 (Aboriginal and or Torres Strait Islanders)"
    value="metric_value"
    fmt="0.0%"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>

<!-- <BigValue
    data={aparent_retention_rate_10_to_12}
    title="Aparent retention rate 10 to 12"
    value="metric_value__latest_year"
    fmt="0.0%"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={aparent_retention_rate_10_to_12}
    title="Aparent retention rate 10 to 12"
    value="metric_value"
    fmt="0.0%"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={aparent_retention_rate_10_to_12_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>

<!-- <BigValue
    data={aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders}
    title="Aparent retention rate 10 to 12 (Aboriginal and or Torres Strait Islanders)"
    value="metric_value__latest_year"
    fmt="0.0%"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->

<BigValue
    data={aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders}
    title="Aparent retention rate 10 to 12 (Aboriginal and or Torres Strait Islanders)"
    value="metric_value"
    fmt="0.0%"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>

<LineBreak/>

<!-- <BigValue
    data={apprenticeship_traineeship_training_contract_approvals}
    title="Apprenticeship traineeship - Approvals"
    value="metric_value__latest_year"
    fmt="#,##0;"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={apprenticeship_traineeship_training_contract_approvals}
    title="Apprenticeship traineeship - Approvals"
    value="metric_value"
    fmt="#,##0;"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={apprenticeship_traineeship_training_contract_approvals_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>

<!-- <BigValue
    data={apprenticeship_traineeship_training_contract_completions}
    title="Apprenticeship traineeship - Completions"
    value="metric_value__latest_year"
    fmt="#,##0;"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={apprenticeship_traineeship_training_contract_completions}
    title="Apprenticeship traineeship - Completions"
    value="metric_value"
    fmt="#,##0;"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={apprenticeship_traineeship_training_contract_completions_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />

<LineBreak/>

<!-- <BigValue
    data={enrolments}
    title="Enrolments"
    value="metric_value__latest_year"
    fmt="#,##0;"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->

<BigValue
    data={enrolments}
    title="Enrolments"
    value="metric_value"
    fmt="#,##0;"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={enrolments_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />

<LineBreak/>

<!-- <BigValue
    data={funding_aud_post_adjustments}
    title="Funding"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={funding_aud_post_adjustments}
    title="Funding - Schools Yearly"
    value="metric_value"
    fmt="$#,##0;"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={funding_aud_post_adjustments_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<!-- <LinkButton  url='/funding'>
  More Details on funding
</LinkButton > -->
<LineBreak/>

<!-- <BigValue
    data={incidents}
    title="Incidents"
    value="metric_value__latest_year"
    fmt="#,##0;"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={incidents}
    title="Incidents"
    value="metric_value"
    fmt="#,##0;"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={incidents_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<LineBreak/>

<!-- <BigValue
    data={school_count}
    title="Schools"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={school_count}
    title="Schools"
    value="metric_value"
    fnt="num0"
  />
<BigValue
    data={school_count_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<!-- <LinkButton  url='/school'>
  More Details on schools
</LinkButton > -->
<LineBreak/>

<!-- <BigValue
    data={staff_count}
    title="Staff"
    value="metric_value__latest_year"
    fmt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={staff_count}
    title="Staff"
    value="metric_value"
    fnt="num0"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={staff_count_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<!-- <LinkButton  url='/staff'>
  More Details on Staff
</LinkButton > -->


<LineBreak/>


<!-- <BigValue
    data={student_count}
    title="Students"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_time__year__latest_year
    comparisonTitle="Latest Refresh"
    comparisonFmt="id"
    comparisonDelta=false
  /> -->
<BigValue
    data={student_count}
    title="Students"
    value="metric_value"
    fnt="num0"
    sparkline=metric_time__year
    sparklineDateFmt="YYYY"
    comparison=metric_value__comp
    comparisonTitle="vs. Last Year"
    comparisonFmt="0.0%"
  />
<BigValue
    data={student_count_latest}
    title="Latest Year"
    value="metric_time__year__latest_year"
    fmt="####"
  />
<!-- <LinkButton  url='/student'>
  More Details on students
</LinkButton > -->
<LineBreak/>




<!-- WIP 🚧 need to be able to not aggregate and just show latest value, but show history with line line -->
<!-- <BigValue
  data={metrics_by_year_saved_query}
  value=metric_value
  title="attendance_rate 🚧"
  lineline=metric_time__year
/> -->

<LineBreak/>

## Goals of this Project


<BigValue
  data={fct__web_analytics_monthly}
  value=total_users
  title="Visualisation Users"
  lineline=event_month
  comparison=prior_month_growth_pct
  comparisonFmt=pct1
  comparisonTitle="vs. Last Month"
/>


<LinkButton  url='/useage'>
  More Details on useage
</LinkButton >
<LineBreak/>
<Alert status="info">

ℹ️ Usage will appear as an error for open source users. I have a seperate workflow that gets usage data requiring API secrets. I dont expose these secrets. So will just show an error when the public are creating the report. But when it goes to production and through CICD we see usage.

</Alert>
<LineBreak/>


  <!-- - attendance_rate
  - apprenticeship_traineeship_training_contract_approvals
  - apprenticeship_traineeship_training_contract_completions
  - class_size_k_6
  - enrolments
  - incidents
  - aparent_retention_rate_7_to_10
  - aparent_retention_rate_10_to_12
  - aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders
  - aparent_retention_rate_7_to_10_aboriginal_and_or_torres_strait_islanders
  - aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders -->


```sql attendance_rate
select * from ${metrics_by_year_saved_query} where metric_name = 'attendance_rate'
```

```sql attendance_rate_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'attendance_rate'
```

```sql aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders
select * from ${metrics_by_year_saved_query} where metric_name = 'aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders'
```

```sql aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'aparent_retention_rate_7_to_12_aboriginal_and_or_torres_strait_islanders'
```

```sql aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders
select * from ${metrics_by_year_saved_query} where metric_name = 'aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders'
```

```sql aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'aparent_retention_rate_10_to_12_aboriginal_and_or_torres_strait_islanders'
```

```sql aparent_retention_rate_10_to_12
select * from ${metrics_by_year_saved_query} where metric_name = 'aparent_retention_rate_10_to_12'
```

```sql aparent_retention_rate_10_to_12_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'aparent_retention_rate_10_to_12'
```

```sql aparent_retention_rate_7_to_10
select * from ${metrics_by_year_saved_query} where metric_name = 'aparent_retention_rate_7_to_10'
```

```sql aparent_retention_rate_7_to_10_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'aparent_retention_rate_7_to_10'
```

```sql apprenticeship_traineeship_training_contract_approvals
select * from ${metrics_by_year_saved_query}  where metric_name = 'apprenticeship_traineeship_training_contract_approvals'
```

```sql apprenticeship_traineeship_training_contract_approvals_latest
select * from ${metrics_by_year_saved_query_latest}  where metric_name = 'apprenticeship_traineeship_training_contract_approvals'
```

```sql apprenticeship_traineeship_training_contract_completions
select * from ${metrics_by_year_saved_query} where metric_name = 'apprenticeship_traineeship_training_contract_completions'
```

```sql apprenticeship_traineeship_training_contract_completions_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'apprenticeship_traineeship_training_contract_completions'
```

```sql enrolments
select * from ${metrics_by_year_saved_query} where metric_name = 'enrolments'
```

```sql enrolments_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'enrolments'
```

```sql incidents
select * from ${metrics_by_year_saved_query} where metric_name = 'incidents'
```

```sql incidents_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'incidents'
```

```sql staff_count
select * from ${metrics_by_year_saved_query} where metric_name = 'staff_count'
```

```sql staff_count_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'staff_count'
```

```sql student_count
select * from ${metrics_by_year_saved_query} where metric_name = 'student_count'
```

```sql student_count_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'student_count'
```

```sql school_count
select * from ${metrics_by_year_saved_query} where metric_name = 'school_count'
```

```sql school_count_latest
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'school_count'
```


```sql funding_aud_post_adjustments
select * from ${metrics_by_year_saved_query} where metric_name = 'funding_aud_post_adjustments'
```

```sql funding_aud_post_adjustments_latest
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
