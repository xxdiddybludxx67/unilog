import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from core.logger import log
from cli.utils import ensure_dir

# You can configure your Azure connection string via environment variable
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING", "")
DEFAULT_CONTAINER = os.getenv("AZURE_CONTAINER", "unilog-logs")


def get_blob_service() -> BlobServiceClient:
    if not AZURE_CONNECTION_STRING:
        raise ValueError("AZURE_CONNECTION_STRING environment variable is not set.")
    return BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)


def upload(file_path: str, container_name: str = None, blob_name: str = None):
    container_name = container_name or DEFAULT_CONTAINER
    blob_name = blob_name or os.path.basename(file_path)

    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return

    try:
        blob_service = get_blob_service()
        container_client: ContainerClient = blob_service.get_container_client(container_name)
        
        # Create container if it does not exist
        try:
            container_client.create_container()
            log(f"Created container: {container_name}")
        except Exception:
            # Container probably already exists
            pass

        blob_client: BlobClient = container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        log(f"Uploaded {file_path} to Azure Blob '{container_name}/{blob_name}'")
    except Exception as e:
        log(f"Azure upload failed for {file_path}: {e}")
