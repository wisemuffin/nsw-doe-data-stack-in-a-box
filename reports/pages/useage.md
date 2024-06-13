
# Usage

<Alert status="info">
The Usage page will help deterine how we are doing on our main quest of getting humans excited about the publically available data curated by NSW Department of Education and our partners.
</Alert>



<BigValue
  data={fct__web_analytics_monthly}
  value=total_users
  title="Visualisation Users"
  sparkline=event_month
  comparison=prior_month_growth_pct
  comparisonFmt=pct1
  comparisonTitle="vs. Last Month"
/>

<Details title="Definitions">

    Users who visit this website.

    *Calculation:*
    Sum of the Users who visit this website

    *Source:*
    google analytics

</Details>

<BigValue
  data={fct__repo_issue_reaction_total}
  value=cnt_reaction
  title="Reactions to Issues"
/>

<Details title="Definitions">

    Reactions such as thumbs up, emojies ect. are recorded on each issue raised against the code repository https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box. This will help understand user engagement

    *Calculation:*
    Sum of reactions to issues raised

    *Source:*
    github

</Details>

## Visualisation Users
📝 Total number of users to visit this data visualisation site on [NSW DOE Data Stack in a Box](https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box/tree/main)

<BarChart
    data={fct__web_analytics}
    x=event_date
    y=total_users
    series=country
    title="Visualisation Users"
/>

## Reactions to Issues
📝 Reactions to issues created on [NSW DOE Data Stack in a Box](https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box/tree/main). This will help us

<CalendarHeatmap
    data={fct__repo_issue_reaction}
    date=created_at_date
    value=cnt_reaction
    title="Reactions to Issues"
    subtitle="Daily Reactions"
/>








```sql fct__repo_issue_reaction
select cnt_reaction,created_at_date, content
from fct__repo_issue_reaction
```

```sql fct__web_analytics
select country, event_date, total_users
from fct__web_analytics
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

```sql fct__repo_issue_reaction_total
select sum(cnt_reaction) as cnt_reaction
from fct__repo_issue_reaction
```
