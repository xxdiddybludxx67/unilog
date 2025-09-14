import os
from google.cloud import storage
from core.logger import log
from cli.utils import ensure_dir

# Configure your GCP environment
GCP_BUCKET = os.getenv("GCP_BUCKET", "unilog-logs")
GCP_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_gcs_client() -> storage.Client:
    if GCP_CREDENTIALS and os.path.exists(GCP_CREDENTIALS):
        return storage.Client.from_service_account_json(GCP_CREDENTIALS)
    else:
        return storage.Client()


def upload(file_path: str, bucket_name: str = None, blob_name: str = None):
    bucket_name = bucket_name or GCP_BUCKET
    blob_name = blob_name or os.path.basename(file_path)

    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return

    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)

        # Create bucket if it does not exist
        if not bucket.exists():
            bucket = client.create_bucket(bucket_name)
            log(f"Created GCS bucket: {bucket_name}")

        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        log(f"Uploaded {file_path} to GCS '{bucket_name}/{blob_name}'")
    except Exception as e:
        log(f"GCS upload failed for {file_path}: {e}")
