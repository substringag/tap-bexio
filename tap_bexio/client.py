"""REST client handling, including bexioStream base class."""

import requests
import logging
from json import JSONDecodeError

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class bexioStream(RESTStream):
    """bexio stream class."""

    url_base = "https://api.bexio.com/"
    item_limit = 1000

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "[]"  # Or override `get_next_page_token`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token")
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        headers["Accept"] = "application/json"
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""

        # Version 1.0 - 3.0 have page information in header.
        # Version >= 4.0 use page information in the response body.

        try:
            resp_dict = response.json()

            if (isinstance(resp_dict, dict)):
                paging = resp_dict.get("paging")
                page = paging.get("page")
                totalPage = paging.get("page_count")

                if (page < totalPage):
                    if (previous_token == None):
                        return 1
                    return page + 1
                else:
                    return None
            else:
                if (previous_token == None):
                    previous_token = 0

                if (response.headers.get("content-length") == "2"):
                    next_page_token = None
                else:
                    next_page_token = previous_token + self.item_limit

                return next_page_token

        except JSONDecoderError:
            # TODO: handle this error better
            logging.warning("JSON decode error occured!")

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["offset"] = next_page_token
            params["limit"] = self.item_limit

            # Contains page if newer API used
            params["page"] = next_page_token

        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
           By default, no payload will be sent (return None).
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
