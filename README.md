# GCP MCP Server 🚀

An MCP (Model Context Protocol) server that enables AI assistants (like GitHub Copilot, Claude) to perform Google Cloud Platform operations via the MCP protocol.

## Overview

This server implements the Model Context Protocol to provide AI assistants with tools for managing GCP resources including:
- Google Kubernetes Engine (GKE) clusters
- Cloud Storage buckets and objects
- Compute Engine VM instances
- IAM policies and bindings

## Supported Operations

| Service | Operations |
|---------|-----------|
| **GKE** | List clusters, Create cluster, Delete cluster, Get cluster details |
| **Cloud Storage** | List buckets, Create bucket, Delete bucket, List objects, Upload object |
| **Compute Engine** | List VMs, Create VM, Delete VM, Start VM, Stop VM |
| **IAM** | Get project IAM policy, Add IAM binding |

## Prerequisites

- **Python 3.10 or higher**
- **Google Cloud SDK** - Install from [cloud.google.com/sdk](https://cloud.google.com/sdk)
- **GCP Authentication** - Set up Application Default Credentials:
  ```bash
  gcloud auth application-default login
  ```
- **GCP Project** - Set a default project:
  ```bash
  gcloud config set project YOUR_PROJECT_ID
  ```
- **Required GCP APIs** - Enable these APIs in your project:
  ```bash
  gcloud services enable container.googleapis.com
  gcloud services enable storage.googleapis.com
  gcloud services enable compute.googleapis.com
  gcloud services enable cloudresourcemanager.googleapis.com
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/manishjindal/gcp-mcp-server.git
   cd gcp-mcp-server
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Server Directly

You can run the server directly from the command line:

```bash
# Using the installed command
gcp-mcp-server

# Or using Python module
python -m gcp_mcp_server.server
```

### Configuring with Claude Desktop

Add the following to your Claude Desktop configuration file (`claude_desktop_config.json`):

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gcp": {
      "command": "python",
      "args": ["-m", "gcp_mcp_server.server"]
    }
  }
}
```

### Configuring with VS Code / GitHub Copilot

#### 1. Create or update `.vscode/mcp.json`:

```json
{
  "servers": {
    "gcp": {
      "command": "python",
      "args": ["-m", "gcp_mcp_server.server"],
      "type": "stdio"
    }
  }
}
```

#### 2. Update VS Code settings (`.vscode/settings.json` or user settings):

```json
{
  "github.copilot.chat.mcp.enabled": true
}
```

## Running Tests

Install pytest if you haven't already:

```bash
pip install pytest
```

Run the test suite:

```bash
pytest tests/ -v
```

## Authentication

This server uses Google Cloud's Application Default Credentials (ADC). You can set up authentication in several ways:

### Option 1: User Credentials (Recommended for Development)
```bash
gcloud auth application-default login
```

### Option 2: Service Account Key
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Option 3: Environment Variables
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### Option 4: Compute Engine / Cloud Run
When running on GCP services, credentials are automatically provided by the metadata server.

## Available Tools

### GKE Tools
1. **list_gke_clusters** - List all GKE clusters in a project
2. **create_gke_cluster** - Create a new GKE cluster
3. **delete_gke_cluster** - Delete a GKE cluster
4. **get_gke_cluster** - Get details of a specific cluster

### Cloud Storage Tools
5. **list_gcs_buckets** - List all Cloud Storage buckets
6. **create_gcs_bucket** - Create a new bucket
7. **delete_gcs_bucket** - Delete a bucket (with optional force delete)
8. **list_gcs_objects** - List objects in a bucket
9. **upload_gcs_object** - Upload content to a bucket

### Compute Engine Tools
10. **list_vm_instances** - List VM instances in a zone
11. **create_vm_instance** - Create a new VM instance
12. **delete_vm_instance** - Delete a VM instance
13. **start_vm_instance** - Start a stopped VM
14. **stop_vm_instance** - Stop a running VM

### IAM Tools
15. **get_project_iam_policy** - Get the IAM policy for a project
16. **add_project_iam_binding** - Add an IAM role binding to a project

## Example Usage with AI Assistants

Once configured, you can ask your AI assistant to perform GCP operations:

- "List all my GKE clusters"
- "Create a Cloud Storage bucket named my-bucket in the US region"
- "List all VM instances in us-central1-a"
- "Show me the IAM policy for my project"

## Project Structure

```
gcp-mcp-server/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .vscode/
│   └── mcp.json
├── src/
│   └── gcp_mcp_server/
│       ├── __init__.py
│       ├── server.py              # Main MCP server entry point
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── gke.py             # GKE cluster operations
│       │   ├── gcs.py             # Cloud Storage operations
│       │   ├── compute.py         # Compute Engine VM operations
│       │   └── iam.py             # IAM operations
│       └── utils/
│           ├── __init__.py
│           └── auth.py            # Authentication helpers
└── tests/
    ├── __init__.py
    ├── test_gke.py
    ├── test_gcs.py
    └── test_compute.py
```

## Security Considerations

- This server requires access to your GCP credentials
- Always review operations before executing them
- Use least-privilege IAM roles when possible
- Consider using service accounts with limited permissions for production use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on the GitHub repository.