import os
import boto3
from botocore.exceptions import ClientError
from core.logger import log
from cli.utils import ensure_dir

# Environment-based configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "unilog-logs")


def get_s3_client():
    """
    Initialize and return an S3 client.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set as environment variables.")
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )


def upload(file_path: str, bucket_name: str = None, object_name: str = None):
    bucket_name = bucket_name or S3_BUCKET
    object_name = object_name or os.path.basename(file_path)

    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return

    try:
        s3_client = get_s3_client()

        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError:
            s3_client.create_bucket(Bucket=bucket_name)
            log(f"Created S3 bucket: {bucket_name}")

        s3_client.upload_file(file_path, bucket_name, object_name)
        log(f"Uploaded {file_path} to S3 '{bucket_name}/{object_name}'")
    except ClientError as e:
        log(f"S3 upload failed for {file_path}: {e}")
