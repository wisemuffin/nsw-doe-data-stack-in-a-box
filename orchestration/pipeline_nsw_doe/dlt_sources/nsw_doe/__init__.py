"""Source that load github issues, pull requests and reactions for a specific repository via customizable graphql query. Loads events incrementally."""

from typing import Iterator, Optional, Sequence

import dlt
from dlt.common.typing import TDataItems
from dlt.sources import DltResource

from pipeline_nsw_doe.dlt_sources.nsw_doe.helpers import get_nsw_doe_data


@dlt.source(max_table_nesting=2)
def nsw_doe_data(access_token: Optional[str] = None) -> Sequence[DltResource]:
    """
    Args:
        access_token (str): The classic or fine-grained access token. If not provided, calls are made anonymously

    Returns:
        DltSource:

    """

    # use naming function in table name to generate separate tables for each event
    @dlt.resource(
        # primary_key="id",
        # table_name=lambda i: "raw_github_events_" + i["type"]
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
        # columns={
        #     "last_online": {"data_type": "timestamp"},
        #     "joined": {"data_type": "timestamp"},
        # },
    )
    def raw__nsw_doe_datansw__enrolments_primary(
        access_token: Optional[str] = access_token,
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
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__enrolments_secondary(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=afee026b-6d18-4cd5-991c-74292db81322"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__enrolments_central(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=12fb9921-1a09-4661-966f-7ec5a5d4f9ab"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__enrolments_ssp(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=5f0736cd-9b26-48e2-a45d-b74c7cbe83ed"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__incidents_2022_part_1(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=7aad21e8-552b-49e1-a667-f99ff8b71f25"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__incidents_2022_part_2(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=413aacee-7673-46de-8d1e-8d0c7e2cb896"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__incidents_2021_part_1(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=aac44f6c-be1e-47f6-b420-c636470fd806"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__incidents_2021_part_2(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=8175de13-eb11-4c87-b886-15a2e6ad4043"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__incidents_2020_part_1(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=a761d9ab-e7b3-4e51-91de-52cc9299ead3"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__incidents_2020_part_2(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=32c6acdc-5192-454a-8bf5-d4597a8b8ea7"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__class_size(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=7616001d-e4cb-4e4a-9a4f-76b166df5d37"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__aparent_retention_rate_10_to_12(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=6c36db3e-ff18-4ff1-a1e1-af5299cade19"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__aparent_retention_rate_7_to_10(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=73529e52-b9ce-492e-a5fa-2e4aaf5993cd"
        ):
            yield page

    @dlt.resource(
        write_disposition="replace",
        schema_contract={
            "tables": "evolve",
            "columns": "evolve",
            "data_type": "freeze",
        },
    )
    def raw__nsw_doe_datansw__aparent_retention_rate_aboriginal_and_or_torres_strait_islanders(
        access_token: Optional[str] = access_token,
    ) -> Iterator[TDataItems]:
        for page in get_nsw_doe_data(
            access_token, "?resource_id=61aa10b5-4f2e-43db-862e-32fde8e8eb82"
        ):
            yield page

    return (
        raw__nsw_doe_datansw__enrolments_primary,
        raw__nsw_doe_datansw__enrolments_secondary,
        raw__nsw_doe_datansw__enrolments_central,
        raw__nsw_doe_datansw__enrolments_ssp,
        raw__nsw_doe_datansw__incidents_2022_part_1,
        raw__nsw_doe_datansw__incidents_2022_part_2,
        raw__nsw_doe_datansw__incidents_2021_part_1,
        raw__nsw_doe_datansw__incidents_2021_part_2,
        raw__nsw_doe_datansw__incidents_2020_part_1,
        raw__nsw_doe_datansw__incidents_2020_part_2,
        raw__nsw_doe_datansw__class_size,
        raw__nsw_doe_datansw__aparent_retention_rate_10_to_12,
        raw__nsw_doe_datansw__aparent_retention_rate_7_to_10,
        raw__nsw_doe_datansw__aparent_retention_rate_aboriginal_and_or_torres_strait_islanders,
    )


# # testing out dlt pipeline without dagster
# # make sure you comment this bit when not testing!!
# pipeline = dlt.pipeline(destination="duckdb", dataset_name="analytics")

# info = pipeline.run(nsw_doe_data())
