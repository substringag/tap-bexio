"""REST client handling, including bexioStream base class."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Iterable

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class bexioStream(RESTStream):
    """bexio stream class."""

    url_base = "https://api.bexio.com/"
<<<<<<< HEAD
    item_limit = 500
    new_paging_system = False
=======
    item_limit = 499
>>>>>>> dev

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

        # Version 1.0 - 2.0 give paging information in the headers. "Content-Length"==2 means no more data
        # Version 3.0 have more paging information in the header: total-count, offset and limit
        # Version >= 4.0 use page information in the response body: page, page_size, page_count and item_count

        logging.debug(f"Previous token: {previous_token}")

        next_page_token = {
            "limit": self.item_limit
        }

        is_version_four = False
        # check if the response is a JSON and has a paging object, if so, it's version 4 o the API
        try:
            response_json = response.json()

            if "paging" in response_json:
                logging.info(f"API Version >= 4.0")
                next_page_token["version"] = 4
                is_version_four = True

                paging = response_json.get("paging")
                page = int(paging.get("page"))
                total_page = int(paging.get("page_count"))

                page_size = int(paging.get("page_size"))
                next_page_token["limit"] = page_size

                logging.debug(f"Last page: {page} | Page size: {page_size} | Total pages: {total_page} | Total items: {paging.get('item_count')}")

                if page < total_page:
                    next_page_token["page"] = page + 1
                else:
                    return None

        except json.decoder.JSONDecodeError:
            logging.error("JSON decode error occured!")
            return None

        if not is_version_four:
            content_length = response.headers.get("content-length")
            total_count = response.headers.get("x-total-count")

            if total_count is None:
                logging.info(f"API Version 1.0 - 2.0")
                next_page_token["version"] = 2

                if content_length == "2":
                    return None  # No more data available

                if previous_token is None:
                    offset = 0
                else:
                    offset = previous_token.get("offset")

                next_page_token["offset"] = offset + self.item_limit

            else:
                logging.info(f"API Version 3.0")
                next_page_token["version"] = 3

                offset = int(response.headers.get("x-offset"))
                limit = int(response.headers.get("x-limit"))

                if offset is not None and limit is not None and total_count is not None:
                    if offset < int(total_count):
                        next_page_token["offset"] = offset + limit
                    else:
                        return None
                else:
                    return None

        return next_page_token

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        if next_page_token:
            logging.debug(f"Next page token: {next_page_token}")

            params["limit"] = next_page_token.get("limit") or self.item_limit
            version = next_page_token.get("version")

            if version == 2:
                params["offset"] = next_page_token.get("offset")

            elif version == 3:
                params["offset"] = next_page_token.get("offset")

            elif version == 4:
                params["page"] = next_page_token.get("page")
                params["limit"] = next_page_token.get("limit")
        else:
            params["page"] = 1
            params["offset"] = 0
            params["limit"] = self.item_limit

        logging.warning(f"URL params: {params}")

        return params

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
<<<<<<< HEAD
            logging.error(" ======> Skipped stream based on minor HTTP status code erro for REST API")
            logging.error(e)
=======
            logging.error("==> Skipped stream based on minor HTTP status code error for REST API (code 400 - 403)")
>>>>>>> dev


class MinorApiException(Exception):
    """Exception to raise when the client response with error code 400 to 403."""
