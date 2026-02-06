"""Tests for Compute Engine tools."""

import json
from unittest.mock import patch, MagicMock
from gcp_mcp_server.tools.compute import list_instances, delete_instance


@patch("gcp_mcp_server.tools.compute.compute_v1.InstancesClient")
@patch("gcp_mcp_server.tools.compute.get_project_id", return_value="test-project")
def test_list_instances(mock_project, mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client

    mock_instance = MagicMock()
    mock_instance.name = "my-vm"
    mock_instance.status = "RUNNING"
    mock_instance.machine_type = "zones/us-central1-a/machineTypes/e2-medium"
    mock_instance.network_interfaces = []

    mock_client.list.return_value = [mock_instance]

    result = json.loads(list_instances())
    assert len(result) == 1
    assert result[0]["name"] == "my-vm"


@patch("gcp_mcp_server.tools.compute.compute_v1.InstancesClient")
@patch("gcp_mcp_server.tools.compute.get_project_id", return_value="test-project")
def test_delete_instance(mock_project, mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_operation = MagicMock()
    mock_client.delete.return_value = mock_operation

    result = json.loads(delete_instance("my-vm"))
    assert result["status"] == "deleted"
