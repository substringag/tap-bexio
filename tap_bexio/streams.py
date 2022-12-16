"""Stream type classes for tap-bexio."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_bexio.client import bexioStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class AccountingJournalStream(bexioStream):
    """AccountingJournal stream."""
    name = "accounting_journal"
    path = "3.0/accounting/journal"  ##3-er API! there the wording is plural 
    data_key = "name"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "accounting_journal.json"


class CurrenciesStream(bexioStream):
    """Currencies stream."""
    name = "currencies"
    path = "3.0/currencies"  ##3-er API! there the wording is plural 
    data_key = "name"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "currencies.json"


class SalutationStream(bexioStream):
    """Salutation stream."""
    name = "salutation"
    path = "2.0/salutation"
    data_key = "salutation"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "salutation.json"


class CompanyProfileStream(bexioStream):
    """Company Profile stream."""
    name = "company_profile"
    path = "2.0/company_profile"
    data_key = "company_profile"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "company_profile.json"



class TitleStream(bexioStream):
    """Title stream."""
    name = "title"
    path = "2.0/title"
    data_key = "title"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "title.json"



class ContactGroupStream(bexioStream):
    """Contact Group stream."""
    name = "contact_group"
    path = "2.0/contact_group"
    data_key = "contact_group"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "contact_group.json"

# this is called "Contact Sectors" in the API Dokumentation, but "contact_branch" in the endpoint. https://docs.bexio.com/legacy/resources/contact_branch/
class ContactBranchStream(bexioStream):
    """Contact Branch stream."""
    name = "contact_branch"
    path = "2.0/contact_branch"
    data_key = "contact_branch"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "contact_branch.json"


class ContactTypeStream(bexioStream):
    """Contact Type stream."""
    name = "contact_types"
    path = "2.0/contact_type"
    data_key = "contact_type"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "contact_type.json"


class ContactStream(bexioStream):
    """Contact stream."""
    name = "contacts"
    path = "2.0/contact"
    data_key = "contact"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "contact.json"


class BusinessActivityStream(bexioStream):
    """Business Activity stream."""
    name = "business_activities"
    path = "2.0/client_service"
    data_key = "business_activity"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "business_activity.json"

class ProjectsStream(bexioStream):
    """Projects stream."""
    name = "projects"
    path = "2.0/pr_project"
    data_key = "project"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "pr_project.json"

class ProjectStatesStream(bexioStream):
    """Projects states stream."""
    name = "project_states"
    path = "2.0/pr_project_state"
    data_key = "project_state"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "pr_project_state.json"

class ProjectTypesStream(bexioStream):
    """Project Types stream."""
    name = "project_types"
    path = "2.0/pr_project_type"
    data_key = "project_type"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "pr_project_type.json"

class TimesheetsStream(bexioStream):
    """Timesheets stream."""
    name = "timesheets"
    path = "2.0/timesheet"
    data_key = "timesheet"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "timesheet.json"

class OfferStream(bexioStream):
    """Offer stream."""
    name = "offer"
    path = "2.0/kb_offer"
    data_key = "offer "
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "kb_offer.json"

class OrderStream(bexioStream):
    """Order stream."""
    name = "order"
    path = "2.0/kb_order"
    data_key = "order "
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "kb_order.json"

class InvoicesStream(bexioStream):
    """Invoices stream."""
    name = "kb_invoices"
    path = "2.0/kb_invoice"
    data_key = "kb_invoices"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "kb_invoice.json"
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "id": record["id"],
        }

# class InvoiceStream(bexioStream):
#     """Invoice stream."""
#     name = "kb_invoice"
#     path = "2.0/kb_invoice/{id}"
#     data_key = "kb_invoice"
#     primary_keys = ["id"]
#     replication_method = "INCREMENTAL"
#     replication_key = "id"
#     schema_filepath = SCHEMAS_DIR / "kb_invoice.json"
#     # EpicIssues streams should be invoked once per parent epic:
#     parent_stream_type = InvoicesStream
#     # Assume epics don't have `updated_at` incremented when issues are changed:
#     ignore_parent_replication_keys = False

class AccountsStream(bexioStream):
    """Accounts stream."""
    name = "accounts"
    path = "2.0/accounts"
    data_key = "accounts"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "accounts.json"

class AccountGroupsStream(bexioStream):
    """Account Groups stream."""
    name = "account_groups"
    path = "2.0/account_groups"
    data_key = "account_groups"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "account_groups.json"
