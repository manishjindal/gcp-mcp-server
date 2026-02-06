"""
Google Cloud Storage (GCS) tools.
"""

import json
from google.cloud import storage
from gcp_mcp_server.utils import get_project_id


def list_buckets(project_id: str | None = None) -> str:
    """List all GCS buckets in a project."""
    project_id = project_id or get_project_id()
    client = storage.Client(project=project_id)

    buckets = []
    for b in client.list_buckets():
        buckets.append({
            "name": b.name,
            "location": b.location,
            "storage_class": b.storage_class,
            "created": b.time_created.isoformat() if b.time_created else None,
        })
    return json.dumps(buckets, indent=2)


def create_bucket(
    bucket_name: str,
    location: str = "US",
    storage_class: str = "STANDARD",
    project_id: str | None = None,
) -> str:
    """Create a new GCS bucket."""
    project_id = project_id or get_project_id()
    client = storage.Client(project=project_id)

    bucket = client.bucket(bucket_name)
    bucket.storage_class = storage_class
    new_bucket = client.create_bucket(bucket, location=location)

    return json.dumps({
        "status": "created",
        "name": new_bucket.name,
        "location": new_bucket.location,
        "storage_class": new_bucket.storage_class,
    }, indent=2)


def delete_bucket(bucket_name: str, force: bool = False) -> str:
    """Delete a GCS bucket. Use force=True to delete non-empty buckets."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    if force:
        blobs = list(bucket.list_blobs())
        bucket.delete_blobs(blobs)

    bucket.delete()
    return json.dumps({
        "status": "deleted",
        "bucket_name": bucket_name,
    }, indent=2)


def list_objects(bucket_name: str, prefix: str | None = None) -> str:
    """List objects in a GCS bucket."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    objects = []
    for blob in bucket.list_blobs(prefix=prefix):
        objects.append({
            "name": blob.name,
            "size_bytes": blob.size,
            "content_type": blob.content_type,
            "updated": blob.updated.isoformat() if blob.updated else None,
        })
    return json.dumps(objects, indent=2)


def upload_object(
    bucket_name: str,
    object_name: str,
    content: str,
    content_type: str = "text/plain",
) -> str:
    """Upload a string content as an object to a GCS bucket."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(content, content_type=content_type)

    return json.dumps({
        "status": "uploaded",
        "bucket": bucket_name,
        "object": object_name,
        "size_bytes": blob.size,
    }, indent=2)
