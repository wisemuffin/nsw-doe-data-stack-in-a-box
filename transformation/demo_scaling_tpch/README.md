# duckdb tpch docs

https://duckdb.org/docs/extensions/tpch

# Setup
```bash
duckdb dev.duckdb
ATTACH 'my_catalog.db' AS my_catalog;

CALL dbgen(sf = 1);
```


```bash
task duck
CREATE SCHEMA tpch;
USE main;
CALL dbgen(sf = 1);
```

```sql
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS lineitem;
DROP TABLE IF EXISTS nation;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS partsupp;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS supplier;
```

generate a lot of data
```bash
CALL dbgen(sf = 50, children = 100, step = 0);
```


# metriflow examples

```bash
dbt parse
mf query --metrics gross_item_sales_amount --group-by metric_time__year
mf query --saved-query order_metrics
```
