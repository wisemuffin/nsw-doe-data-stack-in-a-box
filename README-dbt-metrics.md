Validation (normally both of these steps are done in cloud but locally need to run both)
```bash
dbt compile 
mf validate-configs   
```

`dbt parse` doesnt hit warehouse just parses also doesnt seem to know about meitrcs. `dbt combile` does hit wh and adds metrics to ./target folder.