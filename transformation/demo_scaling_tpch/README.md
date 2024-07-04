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
