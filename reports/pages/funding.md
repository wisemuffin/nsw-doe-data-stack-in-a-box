
# Overview

<BigValue
    data={funding_aud_post_adjustments}
    title="Funding"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_value__comp
    comparisonTitle="prior year growth"
    comparisonFmt="pct"
  />

  <BigValue
    data={funding_aud_post_adjustments}
    title="Latest Refresh"
    value="metric_time__year__latest_year"
    fmt="id"
    comparison=metric_time__year__prior_year
    comparisonTitle="prior year"
    comparisonDelta=false
    comparisonFmt="id"
  />

<Details title="Definitions">

    The Resource Allocation Model (RAM) was developed to ensure a fair, efficient and transparent allocation of the state public education budget for every school. The model recognises that students and school communities are not all the same and that they have different needs which require different levels of support.

    More info: https://education.nsw.gov.au/about-us/strategies-and-reports/schools-funding/resource-allocation-model

    *Calculation:*
    Sum of the funding accross all New South Wales, Australian public schools

    *Source:*
    https://data.nsw.gov.au/

</Details>

# Over Time

<BarChart
  data={metrics_by_year_saved_query}
  x=metric_time__year
  y=funding_aud_post_adjustments
  fillColor="#488f96"
>
  <ReferenceArea xMin="2020-03-15" xMax="2021-05-15" label="COVID Impacted" color=red/>
</BarChart>

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
