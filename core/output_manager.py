# Compatibility function for cli/tail.py
def send_to_output(records, output_type):
    OutputManager([output_type]).write(records)
import os
from typing import List, Dict, Optional
from core.logger import log
from outputs import json_output
from outputs import csv_output
from outputs import parquet_output
from outputs import elastic_output
from cloud import s3, gcp, azure

# Default output directory
OUTPUT_DIR = os.getenv("UNILOG_OUTPUT_DIR", "./output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Supported output types
SUPPORTED_OUTPUTS = ["json", "csv", "parquet", "elastic", "s3", "gcp", "azure"]


class OutputManager:
    def __init__(self, outputs: Optional[List[str]] = None):
        # If no outputs specified, default to all local outputs
        self.outputs = outputs or ["json", "csv", "parquet"]

    def write(self, records: List[Dict], file_name: Optional[str] = None):
        if not records:
            log("No records to write.", level="WARNING")
            return

        file_name = file_name or "unilog_export"

        for output_type in self.outputs:
            try:
                if output_type == "json":
                    path = os.path.join(OUTPUT_DIR, f"{file_name}.json")
                    json_output.write(records, path)
                    log(f"Wrote JSON output to {path}")

                elif output_type == "csv":
                    path = os.path.join(OUTPUT_DIR, f"{file_name}.csv")
                    csv_output.write(records, path)
                    log(f"Wrote CSV output to {path}")

                elif output_type == "parquet":
                    path = os.path.join(OUTPUT_DIR, f"{file_name}.parquet")
                    parquet_output.write(records, path)
                    log(f"Wrote Parquet output to {path}")

                elif output_type == "elastic":
                    elastic_output.write(records)
                    log(f"Wrote output to ElasticSearch")

                elif output_type == "s3":
                    path = os.path.join(OUTPUT_DIR, f"{file_name}.json")
                    json_output.write(records, path)
                    s3.upload(path)
                    log(f"Uploaded {path} to AWS S3")

                elif output_type == "gcp":
                    path = os.path.join(OUTPUT_DIR, f"{file_name}.json")
                    json_output.write(records, path)
                    gcp.upload(path)
                    log(f"Uploaded {path} to GCP")

                elif output_type == "azure":
                    path = os.path.join(OUTPUT_DIR, f"{file_name}.json")
                    json_output.write(records, path)
                    azure.upload(path)
                    log(f"Uploaded {path} to Azure")

                else:
                    log(f"Unsupported output type: {output_type}", level="WARNING")

            except Exception as e:
                log(f"Failed to write {output_type} output: {e}", level="ERROR")
