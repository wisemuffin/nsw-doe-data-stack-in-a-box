
# Overview


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
    fmt="id"
    comparison=metric_time__year__prior_year
    comparisonTitle="prior year" 
    comparisonDelta=false
    comparisonFmt="id"
  />

<Details title="Definitions">
    
    Definition of metrics in Solutions Targets

    ### Time to Proposal

    Average number of days it takes to create a proposal for a customer

    *Calculation:*
    Sum of the number of days it took to create each proposal, divided by the number of proposals created

    *Source:*
    Hubspot

</Details>

# Over Time

<BarChart 
  data={metrics_by_year_saved_query} 
  x=metric_time__year
  y=student_count 
  fillColor="#488f96"
>
  <ReferenceArea xMin="2020-03-15" xMax="2021-05-15" label="COVID Impacted" color=red/>
</BarChart>

```sql student_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'student_count'
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
