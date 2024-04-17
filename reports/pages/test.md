---
title: testing source queries
queries:
    - select1.sql
    - select1_alias: select1.sql
---

note you need to run

```bash
npm run sources -- --changed  
```

evidence docs says this should run automatically in dev mode. but i have to run the above to get it to work.

## tests

```sql aaa
from nsw_doe_data_stack_in_a_box__dev.metrics_by_year_saved_query_latest
```

<DataTable data="{aaa}" search="true" />

```sql bbb
from nsw_doe_data_stack_in_a_box__dev.metrics_by_year_saved_query
```

<DataTable data="{bbb}" search="true" />

