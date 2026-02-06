"""
Google Kubernetes Engine (GKE) tools.
"""

import json
from google.cloud import container_v1
from gcp_mcp_server.utils import get_project_id


def list_clusters(project_id: str | None = None, location: str = "-") -> str:
    """List all GKE clusters in a project."""
    project_id = project_id or get_project_id()
    client = container_v1.ClusterManagerClient()
    parent = f"projects/{project_id}/locations/{location}"

    response = client.list_clusters(parent=parent)
    clusters = []
    for c in response.clusters:
        clusters.append({
            "name": c.name,
            "location": c.location,
            "status": container_v1.Cluster.Status(c.status).name,
            "node_count": c.current_node_count,
            "kubernetes_version": c.current_master_version,
            "endpoint": c.endpoint,
        })
    return json.dumps(clusters, indent=2)


def create_cluster(
    cluster_name: str,
    location: str = "us-central1",
    node_count: int = 3,
    machine_type: str = "e2-medium",
    project_id: str | None = None,
) -> str:
    """Create a new GKE cluster."""
    project_id = project_id or get_project_id()
    client = container_v1.ClusterManagerClient()
    parent = f"projects/{project_id}/locations/{location}"

    cluster = container_v1.Cluster(
        name=cluster_name,
        initial_node_count=node_count,
        node_config=container_v1.NodeConfig(machine_type=machine_type),
    )

    request = container_v1.CreateClusterRequest(parent=parent, cluster=cluster)
    operation = client.create_cluster(request=request)

    return json.dumps({
        "status": "creating",
        "cluster_name": cluster_name,
        "location": location,
        "node_count": node_count,
        "machine_type": machine_type,
        "operation": operation.name,
    }, indent=2)


def delete_cluster(
    cluster_name: str,
    location: str = "us-central1",
    project_id: str | None = None,
) -> str:
    """Delete a GKE cluster."""
    project_id = project_id or get_project_id()
    client = container_v1.ClusterManagerClient()
    name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}"

    operation = client.delete_cluster(name=name)
    return json.dumps({
        "status": "deleting",
        "cluster_name": cluster_name,
        "operation": operation.name,
    }, indent=2)


def get_cluster(
    cluster_name: str,
    location: str = "us-central1",
    project_id: str | None = None,
) -> str:
    """Get details of a specific GKE cluster."""
    project_id = project_id or get_project_id()
    client = container_v1.ClusterManagerClient()
    name = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}"

    c = client.get_cluster(name=name)
    return json.dumps({
        "name": c.name,
        "location": c.location,
        "status": container_v1.Cluster.Status(c.status).name,
        "node_count": c.current_node_count,
        "kubernetes_version": c.current_master_version,
        "endpoint": c.endpoint,
        "network": c.network,
        "subnetwork": c.subnetwork,
        "cluster_ipv4_cidr": c.cluster_ipv4_cidr,
    }, indent=2)
