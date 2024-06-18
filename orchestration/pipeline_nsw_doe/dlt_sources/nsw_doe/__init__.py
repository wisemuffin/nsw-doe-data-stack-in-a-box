"""Source that load github issues, pull requests and reactions for a specific repository via customizable graphql query. Loads events incrementally."""

from typing import Iterator, Optional, Sequence

import dlt
from dlt.common.typing import TDataItems
from dlt.sources import DltResource

from pipeline_nsw_doe.dlt_sources.nsw_doe.helpers import get_nsw_doe_data


@dlt.source(max_table_nesting=2)
def nsw_doe_enrolments(access_token: Optional[str] = None) -> Sequence[DltResource]:
    """
    Args:
        access_token (str): The classic or fine-grained access token. If not provided, calls are made anonymously

    Returns:
        DltSource:

    """
    return (
        raw__nsw_doe_datahub__enrolments_primary(access_token),
        raw__nsw_doe_datahub__enrolments_secondary(access_token),
        raw__nsw_doe_datahub__enrolments_central(access_token),
        raw__nsw_doe_datahub__enrolments_ssp(access_token),
    )


# use naming function in table name to generate separate tables for each event
@dlt.resource(
    # primary_key="id",
    # table_name=lambda i: "raw_github_events_" + i["type"]
    write_disposition="replace",
    # columns={
    #     "last_online": {"data_type": "timestamp"},
    #     "joined": {"data_type": "timestamp"},
    # },
)
def raw__nsw_doe_datahub__enrolments_primary(
    access_token: Optional[str] = None,
    # last_created_at: dlt.sources.incremental[str] = dlt.sources.incremental(
    #     "created_at", initial_value="1970-01-01T00:00:00Z", last_value_func=max
    # ),
) -> Iterator[TDataItems]:
    for page in get_nsw_doe_data(
        access_token, "?resource_id=7a662477-3585-42ba-8e19-1387d6790588"
    ):
        yield page

        # # stop requesting pages if the last element was already older than initial value
        # # note: incremental will skip those items anyway, we just do not want to use the api limits
        # if last_created_at.start_out_of_range:
        #     print(
        #         f"Overlap with previous run created at {last_created_at.initial_value}"
        #     )
        #     break


@dlt.resource(
    write_disposition="replace",
)
def raw__nsw_doe_datahub__enrolments_secondary(
    access_token: Optional[str] = None,
) -> Iterator[TDataItems]:
    for page in get_nsw_doe_data(
        access_token, "?resource_id=afee026b-6d18-4cd5-991c-74292db81322"
    ):
        yield page


@dlt.resource(
    write_disposition="replace",
)
def raw__nsw_doe_datahub__enrolments_central(
    access_token: Optional[str] = None,
) -> Iterator[TDataItems]:
    for page in get_nsw_doe_data(
        access_token, "?resource_id=12fb9921-1a09-4661-966f-7ec5a5d4f9ab"
    ):
        yield page


@dlt.resource(
    write_disposition="replace",
)
def raw__nsw_doe_datahub__enrolments_ssp(
    access_token: Optional[str] = None,
) -> Iterator[TDataItems]:
    for page in get_nsw_doe_data(
        access_token, "?resource_id=5f0736cd-9b26-48e2-a45d-b74c7cbe83ed"
    ):
        yield page


# # testing out dlt pipeline without dagster
# # make sure you comment this bit when not testing!!
# pipeline = dlt.pipeline(destination="duckdb", dataset_name="nsw_doe_data")

# info = pipeline.run(nsw_doe_enrolments(), table_name="nsw_doe_enrolments")
