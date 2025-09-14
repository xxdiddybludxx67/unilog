import time
from pathlib import Path
from core.parser_manager import get_parser
from core.filter import apply_filter
from core.output_manager import send_to_output
from ml.anomaly_detection import detect as detect_anomalies
from core.logger import log


class LogTailer:
    def __init__(self, file_paths, parser_type="generic", output_type="json", enable_ml=False, interval=1.0):
        self.file_paths = [Path(f) for f in file_paths]
        self.parser_type = parser_type
        self.output_type = output_type
        self.enable_ml = enable_ml
        self.interval = interval
        self.parsed_data = []
        self.file_positions = {f: 0 for f in self.file_paths}

    def tail_file(self, file_path):
        try:
            with file_path.open("r", encoding="utf-8") as f:
                f.seek(self.file_positions[file_path])
                new_lines = f.readlines()
                self.file_positions[file_path] = f.tell()
            return new_lines
        except Exception as e:
            log(f"Error tailing file {file_path}: {e}")
            return []

    def parse_lines(self, lines):
        parser = get_parser(self.parser_type)
        for line in lines:
            try:
                record = parser(line)
                filtered = apply_filter(record)
                if filtered:
                    self.parsed_data.append(filtered)
            except Exception as e:
                log(f"Error parsing line: {line.strip()} | Exception: {e}")

    def run_ml(self):
        if self.enable_ml and self.parsed_data:
            log("Running anomaly detection on tailed data")
            anomalies = detect_anomalies(self.parsed_data)
            log(f"Detected {len(anomalies)} anomalies")
            return anomalies
        return []

    def send_output(self):
        if not self.parsed_data:
            return
        send_to_output(self.parsed_data, self.output_type)
        log(f"Sent {len(self.parsed_data)} records to {self.output_type}")
        self.parsed_data = []

    def run(self):
        log(f"Starting log tailing on {len(self.file_paths)} files...")
        try:
            while True:
                for file_path in self.file_paths:
                    new_lines = self.tail_file(file_path)
                    if new_lines:
                        self.parse_lines(new_lines)
                        self.run_ml()
                        self.send_output()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            log("Log tailing stopped by user")
        except Exception as e:
            log(f"Unexpected error in log tailing: {e}")


def tail_logs(file_paths=None, parser_type="generic", output_type="json", enable_ml=False, interval=1.0):
    if file_paths is None:
        file_paths = ["./logs/sample.log"]

    log(f"Starting tail with parser={parser_type}, output={output_type}, ML={enable_ml}, interval={interval}s")
    tailer = LogTailer(file_paths, parser_type, output_type, enable_ml, interval)
    tailer.run()
