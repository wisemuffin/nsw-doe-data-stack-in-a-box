
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
  "FCT__REPO_ISSUE_REACTION" {
    varchar _meta__fct__repo_issue_reaction__sk
  }
  "FCT__RESOURCE_ALLOCATION" {
    varchar _meta__fct__resource_allocation__sk
    varchar _meta__dim__school__sk
    varchar _meta__dim__date__sk
  }
  "FCT__SCHOOL" {
    varchar _meta__fct__school__sk
    varchar _meta__dim__school__sk
  }
  "FCT__STAFF" {
    varchar _meta__fct__staff__sk
  }
  "FCT__STUDENT" {
    varchar _meta__fct__student__sk
  }
  "FCT__WEB_ANALYTICS" {
  }
  "FCT__RESOURCE_ALLOCATION" }|--|| "DIM__SCHOOL": _meta__dim__school__sk
  "FCT__SCHOOL" }|--|| "DIM__SCHOOL": _meta__dim__school__sk

```
