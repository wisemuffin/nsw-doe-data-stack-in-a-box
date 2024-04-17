---
title: Welcome to Evidence
---

## NSW Public Schools Overview

<Alert status="info">
Note about visuals below: Evidence's card visuals are a bit limited. So have had to use 2 cards to show the latest refresh date for each metric.
</Alert>

### Staff

<BigValue 
    data={staff_count} 
    title="Staff count"
    value="metric_value__latest_year" 
    comparison=metric_value__comp
    comparisonTitle="prior year growth" 
    comparisonFmt="pct"
  />

  <BigValue 
    data={staff_count} 
    title="Latest Refresh"
    value="metric_time__year__latest_year" 
    fmt="yyyy"
    comparison=metric_time__year__prior_year
    comparisonTitle="prior year" 
    comparisonDelta=false
  />


Value of metric_value__latest_year: 
<Value 
    data={staff_count}
    column=metric_value__latest_year 
    row=0
/>

<!-- <Delta data={staff_count} column=metric_value__comp fmt=pct1 /> -->


<Details title="Definitions">
    
    Definition of metrics in Solutions Targets

    ### Time to Proposal

    Average number of days it takes to create a proposal for a customer

    *Calculation:*
    Sum of the number of days it took to create each proposal, divided by the number of proposals created

    *Source:*
    Hubspot

</Details>



<BigLink href='/staff'>
  More Details 🚧
</BigLink>

<BarChart 
  data={metrics_by_year_saved_query} 
  x=metric_time__year
  y=staff_count 
  fillColor="#488f96"
>
  <ReferenceArea xMin="2020-03-15" xMax="2021-05-15" label="COVID Impacted" color=red/>
</BarChart>

```sql staff_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'staff_count'
```

<BigValue 
    data={student_count} 
    title="Student count"
    value="metric_value__latest_year"
    fnt="num0"
    comparison=metric_value__comp
    comparisonTitle="prior year growth" 
    comparisonFmt="pct"
  />

  <BigValue 
    data={student_count} 
    title="Latest Refresh"
    value="metric_time__year__latest_year" 
    fmt="yyyy"
    comparison=metric_time__year__prior_year
    comparisonTitle="prior year" 
    comparisonDelta=false
  />

```sql student_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'student_count'
```

<BigValue 
    data={school_count} 
    title="School count"
    value="metric_value__latest_year" 
    fnt="num0"
    comparison=metric_value__comp
    comparisonTitle="prior year growth" 
    comparisonFmt="pct"
  />

  <BigValue 
    data={school_count} 
    title="Latest Refresh"
    value="metric_time__year__latest_year" 
    fmt="yyyy"
    comparison=metric_time__year__prior_year
    comparisonTitle="prior year" 
    comparisonDelta=false
  />

```sql school_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'school_count'
```



<Alert status="warning">
This is a warning alert
</Alert>

<BigValue data={metrics_by_year_saved_query} value="funding_aud_post_adjustments"/>
<BigValue data={metrics_by_year_saved_query} value="funding_aud_original"/>
<BigValue data={metrics_by_year_saved_query} value="staff_count"/>
<BigValue data={metrics_by_year_saved_query} value="student_count"/>

## Metrics Consolidated Ref
<DataTable data="{metrics_by_year_saved_query_latest}" search="true" />

## Data
```sql metrics_by_year_saved_query
select * from metrics_by_year_saved_query
```
```sql metrics_by_year_school_saved_query
from metrics_by_year_school_saved_query
```

```sql metrics_by_year_saved_query_latest
from metrics_by_year_saved_query_latest
```
