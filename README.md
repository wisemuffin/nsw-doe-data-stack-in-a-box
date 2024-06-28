<!-- ![NSW Department of Education logo](.github/static/nsw-doe.png) -->

<img src=".github/static/nsw-doe.png" width="150" >


# Welcome to New South Wales Department of Education (NSW DOE) data stack in a box

![Prod CI Checks](https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box/actions/workflows/ci_prod_deploy.yml/badge.svg)
<!-- [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![dbt](https://img.shields.io/badge/dbt-orange)](https://www.getdbt.com/)
[![dagster](https://img.shields.io/badge/dagster-purple)](https://dagster.io/) -->



This is an data-stack-in-a-box based data from [NSW Education Data](https://data.nsw.gov.au/). With the push of one button you can have your own data stack!


## TL;DR - What have we achieved?

### Data Stack

> [!IMPORTANT]
> Click below 👇🏼 to setup your own free data stack packed with [NSW Department of Education](https://education.nsw.gov.au/) data.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/wisemuffin/nsw-doe-data-stack-in-a-box?quickstart=1)


### Reports
This dashboard contains all the metrics we have collected in this data stack project. It uses a visualisation as code tool called [evidence.dev](https:evidence.dev).

[![Dashboard - evidence.dev]][Report]

## Objectives

### Main quests
[NSW Department of Education](https://education.nsw.gov.au/) data stack in a box has two objectives:
1)	Getting humans excited about the publically available data curated by NSW Department of Education and our partners.
2)	Simple one click totaly free 💲 datastack, aiding in learning and proof of concepts.


### Side quests
- Level up our data stack by demoing features in the data stack that we are lacking or need to improve in [NSW Department of Education](https://education.nsw.gov.au/). These demos will start the conversation on what features we want to prioritise.
- Help identify engineering talent during the interview phase by using the project as a case study
- Help identify data quality and reliability issues with our data. This project is being run daily.


## Audience
The project is designed to be very simple when getting started but allows you to go as deep you like!
- **I want to analyse and gain insights into the data.** With the infrastructure free and deployed in one click you don’t need to worry about any implementation details. You can skip straight to analysing and training ML models on top of your own local warehouse.
- **Interested in modelling via SQL?** We got you covered with a environment setup for DBT.
- **Love DevOps and platform engineering?** Check out our Orchestration, CICD pipelines, and automation such as linting, ect.


## Overview of Data Stack (Architecture) 🥨


![Data Architecture](.github/static/architecture.png)


> ![Info] We are simply going to extract data from the [NSW Education Data](https://data.nsw.gov.au/) and load it into our in memory data warehouse 🦆, model, clean, and analyse our data.
> behind the scenes uses https://ckan.org/ an open source data management system used by the likes of [Government of Canada](https://www.canada.ca/en.html), [NHS](https://www.nhs.uk/), [USAs Open Data](https://data.gov/).


> [!WARNING]
> Some of the datasets from ACARA and NSW DOE are based on static urls. These URLs make it challenging to manage future releases of data without manually identifiing the URLs for new data. I will try to keep an eye out for this every few months. 🚧 TODO setup discussion on limitations with public datasets.


<!-- ## Option tooling (Architecture) 🥨

> ![Info] These components are purley for demoing purposes. They are not needed in the project.

- Tableau
  - ai monitoring
- Power BI
- Open Metadata
- DBT Cloud
  - semantic layer
  - column level linage
-->

## Information Management
### Data Catalog
🚧 TODO likley openmetadata see [example](https://sandbox.open-metadata.org/table/RedshiftProd.dev.demo_dbt_jaffle.customers/lineage)

### Conceptual Data Model

```mermaid
erDiagram
    "STUDENT" {
        int student_id
        string name
        date date_of_birth
        string gender
        int school_id
    }
    STAFF {
        int staff_id
        string name
        string role
        date date_of_birth
        int school_id
    }
    COURSE {
        int course_id
        string course_name
        string description
        int school_id
    }
    ENROLLMENT {
        int enrollment_id
        int student_id
        int course_id
        date enrollment_date
    }
    CLASS {
        int class_id
        int course_id
        int staff_id
        string class_room
        date class_time
        int class_size
    }
    SCHOOL {
        int school_id
        string school_name
        string address
    }
    NAPLAN {
        int naplan_id
        int student_id
        date test_date
        string test_type
        int score
    }
    %% HSC {
    %%     int hsc_id
    %%     int student_id
    %%     date exam_date
    %%     string subject
    %%     int score
    %% }
    INCIDENT {
        int incident_id
        int school_id
        date incident_date
        string incident_type
        string description
    }
    ATTENDANCE {
        int attendance_id
        int student_id
        date attendance_date
        bool present
    }
    RETENTION {
        int retention_id
        int school_id
        int year
        float retention_rate
    }
    EARLY_CHILDHOOD_EDU {
        int ece_id
        int school_id
        string program_name
        string description
    }
    UNIVERSITY {
        int university_id
        string university_name
        string address
    }
    APPRENTICESHIP {
        int apprenticeship_id
        int student_id
        string trade
        date start_date
        date end_date
    }
    TRAINEESHIP {
        int traineeship_id
        int student_id
        string field
        date start_date
        date end_date
    }
    "STUDENT" ||--o{ ENROLLMENT : enrolls
    COURSE ||--o{ ENROLLMENT : includes
    STAFF ||--o{ CLASS : teaches
    COURSE ||--o{ CLASS : consists_of
    SCHOOL ||--o{ "STUDENT" : has
    SCHOOL ||--o{ STAFF : employs
    SCHOOL ||--o{ COURSE : offers
    "STUDENT" ||--o{ NAPLAN : takes
    %% "STUDENT" ||--o{ HSC : sits
    SCHOOL ||--o{ INCIDENT : reports
    "STUDENT" ||--o{ ATTENDANCE : records
    SCHOOL ||--o{ RETENTION : tracks
    EARLY_CHILDHOOD_EDU ||--o{ "STUDENT"  : provides
    "STUDENT" ||--o{ APPRENTICESHIP : undertakes
    "STUDENT" ||--o{ TRAINEESHIP : participates_in
    "STUDENT" ||--o{ UNIVERSITY : enrolls_in

```
This is a high level overview of the entities that we are going to model in this project.

> [!INFO] Limitation -
The data available publically for each entitity does not go down to a student. In some cases school level data is avaiable. But most entities only have data published at a state wide (NSW) aggregate level.

### Sources

#### Education Sources
🚧 add column for asset checks
| Name          | Method (API, CSV, Excel) | Contract Y/N | Description                            | Source URL |
| ------------- | ----------------- | ------------ | -------------------------------------- | ---------- |
| `Apprenticeship and Traineeship training contract` | Excel | ❌ | Apprenticeships and Traineeships combine formal study of a nationally recognised qualification with on-the-job training. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-f7cba3fc-6e9b-4b8b-b1fd-e7dda9b49001 |
| `Average government primary school class sizes` | API | ❌ | The average class size for each grade is calculated by taking the number of students in all classes that a student from that grade is in (including composite/multi age classes) divided by the total number of classes that includes a student from that grade. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-43438137-084e-4d50-81c0-ce741ea3b37b/details |
| `Early Childhood Education and Care program locations` | API | ❌ | NSW Early Childhood Education and Care program locations | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-c41c950f-043c-45ea-bf84-22d8037b74bb |
| `Enrolments` | API | ❌ | This data shows February census enrolment figures. All enrolments are self-reported in full-time equivalent (FTE) units and include both full-time and part-time students. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-818ae0d8-d7fb-4b62-963c-7263fdb8e1ca |
| `Incidents` | API | ❌ | Incidents in public schools and how the department supports schools through incidents while still protecting the identity of students and staff. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-43438137-084e-4d50-81c0-ce741ea3b37b |
| `Master dataset: NSW government school locations and student enrolment numbers` | CSV | ✅ | The master dataset contains comprehensive information for all government schools in NSW. Data items include school locations, latitude and longitude coordinates, school type, student enrolment numbers, electorate information, contact details and more. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-78c10ea3-8d04-4c9c-b255-bbf8547e37e7 |
|`Resource Allocation Model (RAM)` | CSV | ✅ | The Resource Allocation Model (RAM) was developed to ensure a fair, efficient and transparent allocation of the state public education budget for every school. The model recognises that students and school communities are not all the same and that they have different needs which require different levels of support. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-3ea5010a-89bd-46bf-be2a-13c82cc0e1bb |
|`Staff` | CSV | ❌ | -------------------------------------- | https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia/staff-numbers||
|`Students` | CSV | ❌ | -------------------------------------- | https://www.acara.edu.au/reporting/national-report-on-schooling-in-australia/student-numbers||
| `Student attendance` | CSV | ❌ | This dataset shows the attendance rates for all NSW government schools in Semester One by alphabetical order. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-b558a070-09f5-4941-a140-e60a744327bf |
| `Student retention rates at NSW government schools` | API | ❌ | The full-time apparent retention rate (ARR) measures the proportion of a cohort of full-time students that moves from one grade to the next, based on an expected rate of progression of one grade per year. It does not track individual students through their final years of secondary schooling. | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-c9fd51b3-506d-4707-b607-0b1853654ce6 |
| `University` | API | ❌ | NSW University Locations by campus | https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-0d43537e-429a-4a71-8d12-92d2d45eccd0 |

#### Utilisation Sources
| Name          | Method (API, CSV, Excel) | Contract Y/N | Description                            | Source URL |
| ------------- | ----------------- | ------------ | -------------------------------------- | ---------- |
| `Google Analytics` | API | ❌ | Captures all the traffic to the data visualisation via [evidence.dev](https://nsw-doe-data-stack-in-a-box-prod.evidence.app/) | https://analytics.google.com/analytics/web/?pli=1#/p438587109/reports/intelligenthome |
| `Github` | API | ❌ | Captures all the events that occour with the open source project [nsw-doe-data-stack-in-a-box](https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box)  | https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box |

### Bus Matrix
🚧 add descriptions for facts
| Fact          | Status | Dim School                            | Dim Schoolastic Year| Dim Calendar Year | Description |
| ------------- | ---------------- | -------------------------------------- | --- | --- | ---|
| `Resource Allocation Model (RAM)`  | ✅ | ✅  | ❌ | ✅ |  |
|`Staff` | ✅ | ❌ | ❌ | ✅ ||
|`Students` | ✅ | ❌ | ❌ | ✅ ||
|`Incident` | 🚧 | ❌ | ❌ | ✅ ||
|`Class Size` | 🚧 | ❌ | ❌ | ✅ ||
|`Aparent Retention Rate` | 🚧 | ❌ | ❌ | ✅ | |
|`Early Childhood Education Centre` | 🚧 | ❌ | ❌ | ❌ | |
|`School` | 🚧 | ❌ | ❌ | ❌ | |
|`Attendance` | 🚧 | ✅  | ❌ | ✅ |  Dont have numerator and denominator so cant aggregate this fact table. Could just out disclamer on average of average |
| `Enrolment` | 🚧 | ✅ | ❌ | ✅ |  |
| `University` | 🚧 | ❌ | ❌ | ❌ |  |
| `Apprenticeship and Traineeship training contract` | 🚧 | ❌ | ❌ | ✅ partially |  |
| `Web Analytics` | ✅ | ❌ | ❌ | ✅  |  |
| `Repo Reactions` | ✅ | ❌ | ❌ | ✅  |  |

### ERD

🚧 TODO [Dimensional ERD check out](./ERD.md)

### Give me more data!

#### Data that I want from DOE

- `Number of techers per school` was on the data hub but was removed citing will now be reported by ABS. But ABS data isnt at a school level.

#### Data from ACARA / NESA

- `NAPLAN` and `HSC attainment` by school. Can get NAPLAN by school going to ACARA's [MySchool](https://www.myschool.edu.au/school/41307) but no easy way to get a view for all schools data.



## Contributing

See below. Also checkout the [wiki](https://github.com/wisemuffin/nsw-doe-data-stack-in-a-box/wiki) with this repo for more info on the project.


To submit your code, fork the repository, create a [new branch](https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-branches-in-github-desktop) on your fork, and open a [Pull Request (PR)](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) once your work is ready for review.

In the PR template, please describe the change, including the motivation/context, test coverage, and any other relevant information. Please note if the PR is a breaking change or if it is related to an open GitHub issue.

A Core reviewer will review your PR in around five business days and provide feedback on any changes it requires to be approved. Once approved and all the tests pass, the reviewer will click the Squash and merge button in Github 🥳.

<!-- Your PR is now merged into Dagster! We’ll shout out your contribution in the release notes. -->


### Contributing - Data Analyses & Reporting



to run the report locally simply run:

```bash
task evidence_setup && evidence
task evidence
```

> [!WARNING] make sure that your dagster pipeline isnt running, when running evidence. Also close down the reporting server `ctrl+c` before you start dagster up again via `task dag`. This is due to a limitation with duckdb locking.

### Contributing - Data Science

🚧 TODO - currently data scientists need to know how to work with pipelines. Still experimenting with this. But you can have a go with the examples that already exist in dagster.

### Contributing - Data Modeling

I have been following the gitlab's data team's handbook for modeling, naming convetions and testing.

I am pretty relaxed with standards in this project. But please read through these before developing to help standise the modeling:

- [Enterprise data warehouse](https://handbook.gitlab.com/handbook/business-technology/data-team/platform/edw/)
- Tests
- SQL style guide


Differences to gitlab's data team's handbook:

1) Raw and other schema's 🚧 TODO - simplify CICD have just used one schema, prefix should be enough
2) staging layer added between raw and prep layers.

<!-- - update ERDs. [dbterd](https://dbterd.datnguyen.de) which turns your [dbt relationship data quality checks](https://docs.getdbt.com/docs/build/tests#generic-data-tests) into an ERD.

```bash
dbt docs generate
.venv/bin/python ERD_generation.py
```
-->

make sure you lint your code with `sqlfluff`:
```bash
sqlfluff lint
sqlfluff fix
```


### Contributing - Pipeline Code / Ingestion

Dagster should automatically start in your codespace (give it a couple of mins for the setup to complete). If you have exited dagster simply type `task dag` on the command line to get it running again.

**testing**

We use `pytest`

**debugging dagster**

To debug dagster you should run `dagster dev` in debug mode. This allows you to set breakpoints in vs code. Simply hit `F5` in vscode (just check that your debug config is set to `Dagster: Debug Dagit UI`).

Behind the scenes VSCode is using `launch.json` with the following args to run dagster in debug mode. Then just select the assets in dagster UI to materialise. If you set breakpoints they will be

```json
{
    "name": "dagster dev",
    "type": "python",
    "request": "launch",
    "module": "dagster",
    "args": [
        "dev",
    ],
    "subProcess": true
}
```

This is one of the first things i wish i knew when learning dagster!


<!---------------------------------------------------------------------------->

[Dashboard - evidence.dev]: https://img.shields.io/badge/Dashboard_-_evidence.dev-37a779?style=for-the-badge

[Report]: https://nsw-doe-data-stack-in-a-box-prod.evidence.app/




## Disclaimer

Due to the evolving nature of school information and local enrolment areas, no responsibility can be taken by the NSW Department of Education, or any of its associated departments, if information is relied upon. For example, but not limited to, real estate purchases or rentals where the school intake zone data is used as a reference source.
