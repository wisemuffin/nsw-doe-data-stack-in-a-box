
# Overview


<BigValue
    data={school_count}
    title="School count"
    value="metric_value__latest_year"
    fnt="num0"
  />

  <BigValue
    data={school_count}
    title="Latest Refresh"
    value="metric_time__year__latest_year"
    fmt="id"
  />

<Details title="Definitions">

    Number of public schools in New South Wales, Australia

    *Calculation:*
    Sum of the number of schools


    *Source:*
    https://data.nsw.gov.au/

</Details>


# School Locations 🚧

<Alert status="warning">
Leaflet maps are very buggy at the moment whilst they are in experimental phase. Also limitation on how many schools we can show.
</Alert>

<Dropdown
    data={dim__school}
    name=Level_of_Schooling
    value=Level_of_Schooling
    multiple=false
    defaultValue={['Primary School']}
/>

    <!-- defaultValue={['Primary School']} -->

<LeafletMap
    data={dim__school}
    lat=Latitude
    long=Longitude
    name=School_Name
    tooltipFields={['Street','Town_Suburb','Phone','School_Email', 'Website', 'Level_of_Schooling','Latest_Year_Enrolment_FTE']}
    height=400
/>

<!-- <LeafletMap
    data={dim__school}
    lat=Latitude
    long=Longitude
    name=School_Name
    tooltipFields={['Street','Town_Suburb','Phone','School_Email', 'Website', 'Level_of_Schooling','Latest_Year_Enrolment_FTE']}
    height=500
/> -->


# Over Time 🚧

<!-- <BarChart
  data={metrics_by_year_saved_query}
  x=metric_time__year
  y=school_count
  fillColor="#488f96"
>
  <ReferenceArea xMin="2020-03-15" xMax="2021-05-15" label="COVID Impacted" color=red/>
</BarChart> -->

```sql school_count
select * from ${metrics_by_year_saved_query_latest} where metric_name = 'school_count'
```

```sql dim__school
from dim__school
-- where Level_of_Schooling in '${inputs.Level_of_Schooling.value}'
limit 100
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
