import os
import glob
from typing import List
from core.parser_manager import get_parser
from core.logger import log
from core.output_manager import send_to_output
from cloud.s3 import upload as s3_upload
from cloud.gcp import upload as gcp_upload
from cloud.azure import upload as azure_upload


class LogIngestor:
    def __init__(self, input_dirs: List[str], parser_type: str, output_type: str, cloud_provider: str = None):
        self.input_dirs = input_dirs
        self.parser_type = parser_type
        self.output_type = output_type
        self.cloud_provider = cloud_provider
        self.parsed_data = []

    def scan_files(self):
        log_files = []
        for dir_path in self.input_dirs:
            if not os.path.exists(dir_path):
                log(f"Directory not found: {dir_path}")
                continue
            log_files.extend(glob.glob(os.path.join(dir_path, "*.log")))
        log(f"Found {len(log_files)} log files")
        return log_files

    def parse_files(self, log_files: List[str]):
        parser = get_parser(self.parser_type)
        for file_path in log_files:
            log(f"Parsing file: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        record = parser(line)
                        self.parsed_data.append(record)
            except Exception as e:
                log(f"Error parsing {file_path}: {e}")

    def send_output(self):
        if not self.parsed_data:
            log("No data to send to output")
            return

        send_to_output(self.parsed_data, self.output_type)
        log(f"Sent {len(self.parsed_data)} records to {self.output_type}")

    def upload_cloud(self):
        if not self.cloud_provider:
            return

        file_path = f"output.{self.output_type}"
        if not os.path.exists(file_path):
            log(f"Output file {file_path} not found for cloud upload")
            return

        if self.cloud_provider.lower() == "s3":
            s3_upload(file_path)
        elif self.cloud_provider.lower() == "gcp":
            gcp_upload(file_path)
        elif self.cloud_provider.lower() == "azure":
            azure_upload(file_path)
        else:
            log(f"Unknown cloud provider: {self.cloud_provider}")

    def run(self):
        files = self.scan_files()
        self.parse_files(files)
        self.send_output()
        self.upload_cloud()


def ingest_logs(input_dirs=None, parser_type="generic", output_type="json", cloud_provider=None):
    if input_dirs is None:
        input_dirs = ["./logs"]

    log(f"Starting ingestion with parser={parser_type}, output={output_type}, cloud={cloud_provider}")
    ingestor = LogIngestor(input_dirs, parser_type, output_type, cloud_provider)
    ingestor.run()
    log("Ingestion complete")
