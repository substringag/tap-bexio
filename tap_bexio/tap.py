"""bexio tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_bexio.streams import (
    AccountingJournalStream,
    CurrenciesStream,
    SalutationStream,
    CompanyProfileStream,
    TitleStream,
    ContactGroupStream,
    ContactBranchStream,
    ContactTypeStream,
    ContactStream,
    BusinessActivityStream,
    TimesheetsStream,
    OfferStream,
    OrderStream,
    InvoicesStream,
    AccountsStream,
    AccountGroupsStream,
    ProjectTypesStream,
    ProjectStatesStream,
    ProjectsStream,
    BillStream,
    ExpensesStream
)

STREAM_TYPES = [
    AccountGroupsStream,
    AccountingJournalStream,
    AccountsStream,
    # BillStream, 403
    BusinessActivityStream,
    # CompanyProfileStream, 400
    ContactBranchStream,
    ContactGroupStream,
    ContactTypeStream,
    ContactStream,
    CurrenciesStream,
    # ExpensesStream, 403
    InvoicesStream,
    OfferStream,
    OrderStream,
    # ProjectsStream, 403
    # ProjectTypesStream, 403
    # ProjectStatesStream, 403
    # SalutationStream, 400
    TitleStream,
    # TimesheetsStream 403
]


class Tapbexio(Tap):
    """bexio tap class."""
    name = "tap-bexio"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
