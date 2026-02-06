"""Tests for GKE tools."""

import json
from unittest.mock import patch, MagicMock
from gcp_mcp_server.tools.gke import list_clusters, create_cluster


@patch("gcp_mcp_server.tools.gke.container_v1.ClusterManagerClient")
@patch("gcp_mcp_server.tools.gke.get_project_id", return_value="test-project")
def test_list_clusters(mock_project, mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client

    mock_cluster = MagicMock()
    mock_cluster.name = "my-cluster"
    mock_cluster.location = "us-central1"
    mock_cluster.status = 2  # RUNNING
    mock_cluster.current_node_count = 3
    mock_cluster.current_master_version = "1.28.0"
    mock_cluster.endpoint = "10.0.0.1"

    mock_response = MagicMock()
    mock_response.clusters = [mock_cluster]
    mock_client.list_clusters.return_value = mock_response

    result = json.loads(list_clusters())
    assert len(result) == 1
    assert result[0]["name"] == "my-cluster"


@patch("gcp_mcp_server.tools.gke.container_v1.ClusterManagerClient")
@patch("gcp_mcp_server.tools.gke.get_project_id", return_value="test-project")
def test_create_cluster(mock_project, mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_operation = MagicMock()
    mock_operation.name = "operation-123"
    mock_client.create_cluster.return_value = mock_operation

    result = json.loads(create_cluster("new-cluster"))
    assert result["status"] == "creating"
    assert result["cluster_name"] == "new-cluster"
