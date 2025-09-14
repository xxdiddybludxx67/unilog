import csv
import os
from typing import List, Dict
from datetime import datetime
from core.logger import log

class CSVOutput:
    def __init__(self, output_dir: str = "logs/csv", filename: str = None):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.filename = filename or f"logs_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        self.filepath = os.path.join(self.output_dir, self.filename)
        self.fieldnames = ["timestamp", "level", "message", "data"]
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
            log(f"CSV file created at {self.filepath}")

    def write_logs(self, logs: List[Dict]):
        if not logs:
            return

        with open(self.filepath, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            for log_entry in logs:
                writer.writerow({
                    "timestamp": log_entry.get("timestamp", datetime.utcnow().isoformat()),
                    "level": log_entry.get("level", "INFO"),
                    "message": log_entry.get("message", ""),
                    "data": str({k: v for k, v in log_entry.items() if k not in ["timestamp", "level", "message"]})
                })
        log(f"Wrote {len(logs)} logs to CSV at {self.filepath}")

    def read_logs(self) -> List[Dict]:
        logs = []
        if not os.path.exists(self.filepath):
            log(f"CSV file not found at {self.filepath}", level="WARN")
            return logs

        with open(self.filepath, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert data field back from string to dictionary if possible
                data_str = row.get("data", "{}")
                try:
                    data = eval(data_str) if data_str else {}
                except Exception:
                    data = {}
                logs.append({
                    "timestamp": row.get("timestamp"),
                    "level": row.get("level"),
                    "message": row.get("message"),
                    **data
                })
        return logs
