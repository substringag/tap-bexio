"""REST client handling, including bexioStream base class."""

import requests
import logging
import json

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError

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
            self, token=self.config.get("auth_token")
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

            if isinstance(resp_dict, dict):
                paging = resp_dict.get("paging")
                logging.info(f"Paging: {paging}")

                page = paging.get("page")
                totalPage = paging.get("page_count")
                logging.info(f"Fetched page: {page} of {totalPage}")

                if page < totalPage:
                    if previous_token == None:
                        return 1
                    return page + 1
                else:
                    return None
            else:
                if previous_token == None:
                    previous_token = 0

                content_length = response.headers.get("content-length")
                if content_length == "2":
                    next_page_token = None
                else:
                    next_page_token = previous_token + self.item_limit

                return next_page_token

        except json.decoder.JSONDecodeError:
            # TODO: handle this error better
            logging.warning("JSON decode error occured!")

    def get_url_params(
            self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        offset = 1
        if next_page_token:
            offset = next_page_token

        params["offset"] = offset
        params["limit"] = self.item_limit

        # Contains page if newer API used
        params["page"] = offset

        if not next_page_token:
            params["offset"] = 0
            params["limit"] = self.item_limit

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
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.

        return row

    # REST error handling (400, 403)
    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response.

        Args:
            response: A `requests.Response`_ object.

        Raises:
        .. _requests.Response:
            https://docs.python-requests.org/en/latest/api/#requests.Response
        """

        # TOOD: handle in a better way!!
        if 400 <= response.status_code <= 403:
            msg = (
                f"{response.status_code} Client Error: "
                f"{response.reason} for path: {self.path}"
            )
            logging.error(response.json())
            raise MinorApiException(msg)

        if 404 <= response.status_code < 500:
            msg = (
                f"{response.status_code} Client Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise FatalAPIError(msg)

        elif 500 <= response.status_code < 600:
            msg = (
                f"{response.status_code} Server Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise RetriableAPIError(msg)


    def get_records(self, context: Optional[dict]) -> Iterable[Dict[str, Any]]:
        """Return a generator of row-type dictionary objects.

        Each row emitted should be a dictionary of property names to their values.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            One item per (possibly processed) record in the API.

        copy based on https://github.com/AutoIDM/tap-googleads/pull/19/files
        """
        try:
            for record in self.request_records(context):
                transformed_record = self.post_process(record, context)
                if transformed_record is None:
                    # Record filtered out during post_process()
                    continue
                yield transformed_record
        except MinorApiException as e:
            logging.error(" ======> Skipped stream based on minor HTTP status code erro for REST API")
            logging.error(e)


class MinorApiException(Exception):
    """Exception to raise when the client response with error code 400 to 403."""