"""Stream type classes for tap-bexio."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_bexio.client import bexioStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

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

