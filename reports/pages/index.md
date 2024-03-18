---
title: Welcome to Evidence
---

_Build polished data products with SQL and Markdown_

This demo [connects](/settings) to a local DuckDB file `needful_things.duckdb`.

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