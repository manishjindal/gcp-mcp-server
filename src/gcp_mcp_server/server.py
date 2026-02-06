"""
GCP MCP Server - Main entry point.
Registers all GCP tools and starts the MCP server.
"""

from mcp.server.fastmcp import FastMCP
from gcp_mcp_server.tools import gke, gcs, compute, iam

mcp = FastMCP(
    "gcp-mcp-server",
    description="An MCP server for performing Google Cloud Platform operations",
)


# GKE TOOLS

@mcp.tool()
def list_gke_clusters(project_id: str | None = None, location: str = "-") -> str:
    """
    List all GKE clusters in a GCP project.
    Args:
        project_id: GCP project ID (uses default if not provided)
        location: GCP location/region ("-" for all locations)
    """
    return gke.list_clusters(project_id=project_id, location=location)


@mcp.tool()
def create_gke_cluster(
    cluster_name: str,
    location: str = "us-central1",
    node_count: int = 3,
    machine_type: str = "e2-medium",
    project_id: str | None = None,
) -> str:
    """
    Create a new GKE cluster.
    Args:
        cluster_name: Name for the new cluster
        location: GCP region (e.g., us-central1)
        node_count: Number of nodes (default: 3)
        machine_type: Machine type for nodes (default: e2-medium)
        project_id: GCP project ID (uses default if not provided)
    """
    return gke.create_cluster(
        cluster_name=cluster_name,
        location=location,
        node_count=node_count,
        machine_type=machine_type,
        project_id=project_id,
    )


@mcp.tool()
def delete_gke_cluster(
    cluster_name: str,
    location: str = "us-central1",
    project_id: str | None = None,
) -> str:
    """
    Delete a GKE cluster.
    Args:
        cluster_name: Name of the cluster to delete
        location: GCP region where the cluster is located
        project_id: GCP project ID (uses default if not provided)
    """
    return gke.delete_cluster(
        cluster_name=cluster_name, location=location, project_id=project_id
    )


@mcp.tool()
def get_gke_cluster(
    cluster_name: str,
    location: str = "us-central1",
    project_id: str | None = None,
) -> str:
    """
    Get details of a specific GKE cluster.
    Args:
        cluster_name: Name of the cluster
        location: GCP region where the cluster is located
        project_id: GCP project ID (uses default if not provided)
    """
    return gke.get_cluster(
        cluster_name=cluster_name, location=location, project_id=project_id
    )


# GCS TOOLS

@mcp.tool()
def list_gcs_buckets(project_id: str | None = None) -> str:
    """
    List all Cloud Storage buckets in a GCP project.
    Args:
        project_id: GCP project ID (uses default if not provided)
    """
    return gcs.list_buckets(project_id=project_id)


@mcp.tool()
def create_gcs_bucket(
    bucket_name: str,
    location: str = "US",
    storage_class: str = "STANDARD",
    project_id: str | None = None,
) -> str:
    """
    Create a new Cloud Storage bucket.
    Args:
        bucket_name: Globally unique name for the bucket
        location: Bucket location (e.g., US, EU, us-central1)
        storage_class: Storage class (STANDARD, NEARLINE, COLDLINE, ARCHIVE)
        project_id: GCP project ID (uses default if not provided)
    """
    return gcs.create_bucket(
        bucket_name=bucket_name,
        location=location,
        storage_class=storage_class,
        project_id=project_id,
    )


@mcp.tool()
def delete_gcs_bucket(bucket_name: str, force: bool = False) -> str:
    """
    Delete a Cloud Storage bucket.
    Args:
        bucket_name: Name of the bucket to delete
        force: If True, delete all objects first, then delete the bucket
    """
    return gcs.delete_bucket(bucket_name=bucket_name, force=force)


@mcp.tool()
def list_gcs_objects(bucket_name: str, prefix: str | None = None) -> str:
    """
    List objects in a Cloud Storage bucket.
    Args:
        bucket_name: Name of the bucket
        prefix: Only list objects with this prefix (like a folder path)
    """
    return gcs.list_objects(bucket_name=bucket_name, prefix=prefix)


@mcp.tool()
def upload_gcs_object(
    bucket_name: str,
    object_name: str,
    content: str,
    content_type: str = "text/plain",
) -> str:
    """
    Upload content as an object to a Cloud Storage bucket.
    Args:
        bucket_name: Name of the bucket
        object_name: Name/path for the object in the bucket
        content: String content to upload
        content_type: MIME type of the content
    """
    return gcs.upload_object(
        bucket_name=bucket_name,
        object_name=object_name,
        content=content,
        content_type=content_type,
    )


# COMPUTE ENGINE TOOLS

@mcp.tool()
def list_vm_instances(
    zone: str = "us-central1-a", project_id: str | None = None
) -> str:
    """
    List all Compute Engine VM instances in a zone.
    Args:
        zone: GCP zone (e.g., us-central1-a)
        project_id: GCP project ID (uses default if not provided)
    """
    return compute.list_instances(zone=zone, project_id=project_id)


@mcp.tool()
def create_vm_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    machine_type: str = "e2-medium",
    image_family: str = "debian-12",
    image_project: str = "debian-cloud",
    disk_size_gb: int = 10,
    project_id: str | None = None,
) -> str:
    """
    Create a new Compute Engine VM instance.
    Args:
        instance_name: Name for the VM
        zone: GCP zone (e.g., us-central1-a)
        machine_type: Machine type (e.g., e2-medium, n1-standard-1)
        image_family: OS image family (e.g., debian-12, ubuntu-2204-lts)
        image_project: Project hosting the image (e.g., debian-cloud)
        disk_size_gb: Boot disk size in GB
        project_id: GCP project ID (uses default if not provided)
    """
    return compute.create_instance(
        instance_name=instance_name,
        zone=zone,
        machine_type=machine_type,
        image_family=image_family,
        image_project=image_project,
        disk_size_gb=disk_size_gb,
        project_id=project_id,
    )


@mcp.tool()
def delete_vm_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """
    Delete a Compute Engine VM instance.
    Args:
        instance_name: Name of the VM to delete
        zone: GCP zone where the VM is located
        project_id: GCP project ID (uses default if not provided)
    """
    return compute.delete_instance(
        instance_name=instance_name, zone=zone, project_id=project_id
    )


@mcp.tool()
def start_vm_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """
    Start a stopped Compute Engine VM instance.
    Args:
        instance_name: Name of the VM to start
        zone: GCP zone where the VM is located
        project_id: GCP project ID (uses default if not provided)
    """
    return compute.start_instance(
        instance_name=instance_name, zone=zone, project_id=project_id
    )


@mcp.tool()
def stop_vm_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """
    Stop a running Compute Engine VM instance.
    Args:
        instance_name: Name of the VM to stop
        zone: GCP zone where the VM is located
        project_id: GCP project ID (uses default if not provided)
    """
    return compute.stop_instance(
        instance_name=instance_name, zone=zone, project_id=project_id
    )


# IAM TOOLS

@mcp.tool()
def get_project_iam_policy(project_id: str | None = None) -> str:
    """
    Get the IAM policy for a GCP project.
    Args:
        project_id: GCP project ID (uses default if not provided)
    """
    return iam.get_iam_policy(project_id=project_id)


@mcp.tool()
def add_project_iam_binding(
    member: str,
    role: str,
    project_id: str | None = None,
) -> str:
    """
    Add an IAM role binding to a GCP project.
    Args:
        member: Member (e.g., user:email@example.com, serviceAccount:sa@proj.iam.gserviceaccount.com)
        role: IAM role (e.g., roles/viewer, roles/editor, roles/storage.admin)
        project_id: GCP project ID (uses default if not provided)
    """
    return iam.add_iam_binding(member=member, role=role, project_id=project_id)


# ENTRY POINT

def main():
    """Start the GCP MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
