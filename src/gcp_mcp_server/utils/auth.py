"""
Authentication utilities for GCP MCP Server.
Uses Application Default Credentials (ADC).
"""

import os
import google.auth
from google.auth.credentials import Credentials


def get_credentials() -> tuple[Credentials, str]:
    """
    Returns GCP credentials and the default project ID.

    Ensure you have run:
        gcloud auth application-default login
    or set GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    credentials, project_id = google.auth.default()
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "Could not determine GCP project ID. "
            "Run `gcloud config set project <PROJECT_ID>` "
            "or set the GOOGLE_CLOUD_PROJECT env variable."
        )
    return credentials, project_id


def get_project_id() -> str:
    """Returns the default GCP project ID."""
    _, project_id = get_credentials()
    return project_id
