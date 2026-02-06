"""
Google Compute Engine tools.
"""

import json
from google.cloud import compute_v1
from gcp_mcp_server.utils import get_project_id


def list_instances(
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """List all VM instances in a zone."""
    project_id = project_id or get_project_id()
    client = compute_v1.InstancesClient()

    instances = []
    for instance in client.list(project=project_id, zone=zone):
        instances.append({
            "name": instance.name,
            "status": instance.status,
            "machine_type": instance.machine_type.split("/")[-1],
            "zone": zone,
            "internal_ip": (
                instance.network_interfaces[0].network_i_p
                if instance.network_interfaces
                else None
            ),
            "external_ip": (
                instance.network_interfaces[0].access_configs[0].nat_i_p
                if instance.network_interfaces
                and instance.network_interfaces[0].access_configs
                else None
            ),
        })
    return json.dumps(instances, indent=2)


def create_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    machine_type: str = "e2-medium",
    image_family: str = "debian-12",
    image_project: str = "debian-cloud",
    disk_size_gb: int = 10,
    network: str = "global/networks/default",
    project_id: str | None = None,
) -> str:
    """Create a new Compute Engine VM instance."""
    project_id = project_id or get_project_id()
    client = compute_v1.InstancesClient()

    machine_type_full = f"zones/{zone}/machineTypes/{machine_type}"

    boot_disk = compute_v1.AttachedDisk(
        auto_delete=True,
        boot=True,
        initialize_params=compute_v1.AttachedDiskInitializeParams(
            source_image=f"projects/{image_project}/global/images/family/{image_family}",
            disk_size_gb=disk_size_gb,
        ),
    )

    network_interface = compute_v1.NetworkInterface(
        network=network,
        access_configs=[
            compute_v1.AccessConfig(
                name="External NAT",
                type_="ONE_TO_ONE_NAT",
            )
        ],
    )

    instance = compute_v1.Instance(
        name=instance_name,
        machine_type=machine_type_full,
        disks=[boot_disk],
        network_interfaces=[network_interface],
    )

    request = compute_v1.InsertInstanceRequest(
        project=project_id,
        zone=zone,
        instance_resource=instance,
    )
    operation = client.insert(request=request)
    operation.result()

    return json.dumps({
        "status": "created",
        "name": instance_name,
        "zone": zone,
        "machine_type": machine_type,
    }, indent=2)


def delete_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """Delete a Compute Engine VM instance."""
    project_id = project_id or get_project_id()
    client = compute_v1.InstancesClient()

    operation = client.delete(project=project_id, zone=zone, instance=instance_name)
    operation.result()

    return json.dumps({
        "status": "deleted",
        "name": instance_name,
        "zone": zone,
    }, indent=2)


def start_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """Start a stopped VM instance."""
    project_id = project_id or get_project_id()
    client = compute_v1.InstancesClient()

    operation = client.start(project=project_id, zone=zone, instance=instance_name)
    operation.result()

    return json.dumps({
        "status": "started",
        "name": instance_name,
        "zone": zone,
    }, indent=2)


def stop_instance(
    instance_name: str,
    zone: str = "us-central1-a",
    project_id: str | None = None,
) -> str:
    """Stop a running VM instance."""
    project_id = project_id or get_project_id()
    client = compute_v1.InstancesClient()

    operation = client.stop(project=project_id, zone=zone, instance=instance_name)
    operation.result()

    return json.dumps({
        "status": "stopped",
        "name": instance_name,
        "zone": zone,
    }, indent=2)
