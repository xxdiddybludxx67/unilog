from typing import List
from core.parser_manager import get_parser
from core.filter import apply_filter
from core.output_manager import send_to_output
from ml.anomaly_detection import detect as detect_anomalies
from core.logger import log


class LogParser:
    def __init__(self, parser_type: str = "generic", output_type: str = "json", enable_ml: bool = False):
        self.parser_type = parser_type
        self.output_type = output_type
        self.enable_ml = enable_ml
        self.parsed_data = []

    def parse_lines(self, lines: List[str]):
        parser = get_parser(self.parser_type)
        for line in lines:
            try:
                record = parser(line)
                # Apply filters
                filtered_record = apply_filter(record)
                if filtered_record:
                    self.parsed_data.append(filtered_record)
            except Exception as e:
                log(f"Error parsing line: {line} | Exception: {e}")

    def process_file(self, file_path: str):
        """
        Parse a log file line by line.
        """
        log(f"Processing file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.parse_lines(lines)
        except Exception as e:
            log(f"Failed to process file {file_path}: {e}")

    def run_ml(self):
        if self.enable_ml and self.parsed_data:
            log("Running anomaly detection on parsed data")
            anomalies = detect_anomalies(self.parsed_data)
            log(f"Detected {len(anomalies)} anomalies")
            return anomalies
        return []

    def send_output(self):
        if not self.parsed_data:
            log("No parsed data to output")
            return
        send_to_output(self.parsed_data, self.output_type)
        log(f"Sent {len(self.parsed_data)} records to {self.output_type}")

    def run(self, file_paths: List[str]):
        for path in file_paths:
            self.process_file(path)
        self.run_ml()
        self.send_output()


def parse_logs(file_paths=None, parser_type="generic", output_type="json", enable_ml=False):

    if file_paths is None:
        file_paths = ["./logs/sample.log"]

    log(f"Starting parsing with parser={parser_type}, output={output_type}, ML={enable_ml}")
    parser = LogParser(parser_type, output_type, enable_ml)
    parser.run(file_paths)
    log("Parsing complete")
