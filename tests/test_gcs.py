"""Tests for GCS tools."""

import json
from unittest.mock import patch, MagicMock
from gcp_mcp_server.tools.gcs import list_buckets, create_bucket


@patch("gcp_mcp_server.tools.gcs.storage.Client")
@patch("gcp_mcp_server.tools.gcs.get_project_id", return_value="test-project")
def test_list_buckets(mock_project, mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client

    mock_bucket = MagicMock()
    mock_bucket.name = "my-bucket"
    mock_bucket.location = "US"
    mock_bucket.storage_class = "STANDARD"
    mock_bucket.time_created = None

    mock_client.list_buckets.return_value = [mock_bucket]

    result = json.loads(list_buckets())
    assert len(result) == 1
    assert result[0]["name"] == "my-bucket"


@patch("gcp_mcp_server.tools.gcs.storage.Client")
@patch("gcp_mcp_server.tools.gcs.get_project_id", return_value="test-project")
def test_create_bucket(mock_project, mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client

    mock_bucket = MagicMock()
    mock_bucket.name = "new-bucket"
    mock_bucket.location = "US"
    mock_bucket.storage_class = "STANDARD"
    mock_client.bucket.return_value = mock_bucket
    mock_client.create_bucket.return_value = mock_bucket

    result = json.loads(create_bucket("new-bucket"))
    assert result["status"] == "created"
