
```mermaid
---
title: Dimensional ERD
---
erDiagram
  "DIM__DATE" {
    varchar _meta__dim__date__sk
  }
  "DIM__SCHOOL" {
    varchar _meta__dim__school__sk
  }
  "FCT__RESOURCE_ALLOCATION" {
    varchar _meta__fct__resource_allocation__sk
    varchar _meta__dim__school__sk
  }
  "FCT__RESOURCE_ALLOCATION" }|--|| "DIM__SCHOOL": _meta__dim__school__sk

```
