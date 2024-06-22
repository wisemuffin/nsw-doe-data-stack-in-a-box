from typing import Iterator, List, Optional

from dlt.common.typing import StrAny
from dlt.sources.helpers import requests

from pipeline_nsw_doe.dlt_sources.nsw_doe.settings import (
    RPC_API_BASE_URL,
    RPC_API_DATASEARCH,
)


#
# Shared
#
def _get_auth_header(access_token: Optional[str]) -> StrAny:
    if access_token:
        return {"Authorization": f"Bearer {access_token}"}
    else:
        # REST API works without access token (with high rate limits)
        return {}


#
# Rest API helpers
#

#
# Rest API helpers
# https://data.nsw.gov.au/data?resource_id=7a662477-3585-42ba-8e19-1387d6790588&limit=100
# https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=7a662477-3585-42ba-8e19-1387d6790588


def get_nsw_doe_data(access_token: Optional[str], query: str) -> Iterator[List[StrAny]]:
    def _request(page_url: str) -> requests.Response:
        r = requests.get(page_url, headers=_get_auth_header(access_token))
        print(
            f"got page {page_url}"  # , requests left: " + r.headers["x-ratelimit-remaining"]
        )
        return r

    next_page_enpoint = RPC_API_DATASEARCH + query
    while True:
        r: requests.Response = _request(RPC_API_BASE_URL + next_page_enpoint)
        page_items = r.json()
        if len(page_items["result"]["records"]) == 0:
            break
        yield page_items["result"]["records"]
        # ckan api is rpc rather than rest so cant use r.link see: https://docs.ckan.org/en/2.10/api/index.html
        # if "next" not in r.links:
        if "next" not in page_items["result"]["_links"]:
            break
        next_page_enpoint = page_items["result"]["_links"]["next"]
