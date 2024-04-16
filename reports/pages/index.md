---
title: Welcome to Evidence
---

_Build polished data products with SQL and Markdown_

This demo [connects](/settings) to a local DuckDB file `nsw_doe_data_stack_in_a_box__dev.duckdb`.

```sql dg_test
select
  *
from sq__resource_allocation
```
```sql data_types
select * from data_types
```

```sql metrics_by_year_saved_query
select * from metrics_by_year_saved_query
```
```sql metrics_by_year_school_saved_query
select * from metrics_by_year_school_saved_query
```

```sql metric_by_year_saved_query_latest
-- apply window logic to get latest value
with prep as (
    UNPIVOT nsw_doe_data_stack_in_a_box__dev.metrics_by_year_saved_query
    ON funding_aud_post_adjustments,funding_aud_original,funding_aud_post_adjustments_prev_year,funding_aud_post_adjustments_yoy,staff_count
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
        metric_time__year as metric_time__year__latest_year,
    from prep_rank_period where period_rank=1
),
prior_year as (
    select metric_name, 
        metric_value as metric_value__prior_year, 
        metric_time__year as metric_time__year__prior_year
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
```
<DataTable data="{metric_by_year_saved_query_latest}" search="true" />


```sql staff_count
select * from ${metric_by_year_saved_query_latest} where metric_name = 'staff_count'
```

<DataTable data="{staff_count}" search="true" />

<BigValue data={staff_count} 
  title="Staff count"
  value="metric_value__latest_year" 
  comparison=metric_value__comp
  comparisonTitle="prior year growth" 
  comparisonFmt="pct"
  />

<BigValue data={metrics_by_year_saved_query} value="funding_aud_post_adjustments"/>
<BigValue data={metrics_by_year_saved_query} value="funding_aud_original"/>
<BigValue data={metrics_by_year_saved_query} value="staff_count"/>
<BigValue data={metrics_by_year_saved_query} value="student_count"/>

<BigValue data={dg_test} value="funding_aud_post_adjustments"/>
<BigValue data={dg_test} value="funding_aud_original"/>

<!-- metric_time__year currently a varchar -->
<BigValue data={dg_test} value="funding_aud_original" sparkline=metric_time__year sparklineYScale=false/>

<DataTable data="{dg_test}" search="true" />
<DataTable data="{data_types}" search="true" />

<DataTable data="{orders_by_month}" search="true" />

<LineChart
  data={orders_by_month}
  y=sales
  yFmt=usd0k
  title = "Sales by Month, USD"
/>

## Write in Markdown

Evidence renders markdown files into web pages. This page is:
`[project]/pages/index.md`.

## Run SQL using Code Fences

```sql orders_by_month
select
  date_trunc('month', order_datetime) as order_month,
  count(*) as number_of_orders,
  sum(sales) as sales,
  sum(sales)/count(*) as average_order_value
from orders
where order_datetime >= '2020-01-01'
group by 1 order by 1 desc
```

In your markdown file, you can include SQL queries in code fences. Evidence will run these queries through your database and return the results to the page.

<Alert status=info>  
To see the queries on a page, click the 3-dot menu at the top right of the page and Show Queries. You can see both the SQL and the query results by interacting with the query above.
</Alert>

## Visualize Data with Components

### Value in Text

Last month customers placed **<Value data={orders_by_month} column=number_of_orders/>** orders. The AOV was **<Value data={orders_by_month} column=average_order_value fmt=usd2/>**.

### Big Value 
<BigValue data={orders_by_month} value=sales fmt=usd0/>
<BigValue data={orders_by_month} value=number_of_orders />


### Bar Chart

<BarChart 
  data={orders_by_month} 
  x=order_month
  y=number_of_orders 
  fillColor="#488f96"
>
  <ReferenceArea xMin="2020-03-15" xMax="2021-05-15" label="COVID Impacted" color=red/>
</BarChart>

> **Try:** Change the chart to a `<LineChart>`.

### Data Table

<DataTable data={orders_by_month} rows=6/>

> **More:** See [all components](https://docs.evidence.dev/components/all-components)

## Add Interactive Features

The latest version of Evidence includes features that allow you to easily create interactive data visualizations.

### Chart with Filter 

```sql categories
select
    category
from orders
group by category
```

<Dropdown data={categories} name=category value=category>
    <DropdownOption value="%" valueLabel="All Categories"/>
</Dropdown>

<Dropdown name=year>
    <DropdownOption value=% valueLabel="All Years"/>
    <DropdownOption value=2019/>
    <DropdownOption value=2020/>
    <DropdownOption value=2021/>
</Dropdown>

```sql orders_by_category
select 
    date_trunc('month', order_datetime) as month,
    sum(sales) as sales_usd,
    category
from orders
where category like '${inputs.category.value}'
and date_part('year', order_datetime) like '${inputs.year.value}'
group by all
order by sales_usd desc
```

<BarChart
    data={orders_by_category}
    title="Sales by Month, {inputs.category.label}"
    x=month
    y=sales_usd
    series=category
/>




# Share with Evidence Cloud

Evidence Cloud is the easiest way to securely share your project. 

- Get your project online
- Authenticate users
- Schedule data refreshes

<BigLink href='https://du3tapwtcbi.typeform.com/waitlist?utm_source=template&typeform-source=template'>Deploy to Evidence Cloud &rarr;</BigLink>

You can use Netlify, Vercel or another static hosting provider to [self-host Evidence](https://docs.evidence.dev/deployment/overview).

# Get Support

- Message us on [Slack](https://slack.evidence.dev/)
- Read the [Docs](https://docs.evidence.dev/)
- Open an issue on [Github](https://github.com/evidence-dev/evidence)