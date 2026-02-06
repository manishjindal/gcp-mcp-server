"""
IAM tools for the GCP MCP Server.
"""

import json
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2
from gcp_mcp_server.utils import get_project_id


def get_iam_policy(project_id: str | None = None) -> str:
    """Get the IAM policy for a project."""
    project_id = project_id or get_project_id()
    client = resourcemanager_v3.ProjectsClient()

    request = iam_policy_pb2.GetIamPolicyRequest(
        resource=f"projects/{project_id}",
    )
    policy = client.get_iam_policy(request=request)

    bindings = []
    for binding in policy.bindings:
        bindings.append({
            "role": binding.role,
            "members": list(binding.members),
        })

    return json.dumps({"project": project_id, "bindings": bindings}, indent=2)


def add_iam_binding(
    member: str,
    role: str,
    project_id: str | None = None,
) -> str:
    """
    Add an IAM binding to a project.
    member format: user:email@example.com, serviceAccount:sa@project.iam.gserviceaccount.com
    role format: roles/viewer, roles/editor, etc.
    """
    project_id = project_id or get_project_id()
    client = resourcemanager_v3.ProjectsClient()
    resource = f"projects/{project_id}"

    get_request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
    policy = client.get_iam_policy(request=get_request)

    new_binding = policy_pb2.Binding(role=role, members=[member])
    policy.bindings.append(new_binding)

    set_request = iam_policy_pb2.SetIamPolicyRequest(
        resource=resource, policy=policy
    )
    updated_policy = client.set_iam_policy(request=set_request)

    return json.dumps({
        "status": "binding_added",
        "member": member,
        "role": role,
        "project": project_id,
    }, indent=2)
