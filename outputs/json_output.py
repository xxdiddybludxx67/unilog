import json
import os
from typing import List, Dict
from datetime import datetime
from core.logger import log

class JSONOutput:
    def __init__(self, output_dir: str = "logs/json", filename: str = None):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.filename = filename or f"logs_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        self.filepath = os.path.join(self.output_dir, self.filename)
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
            log(f"JSON file created at {self.filepath}")

    def write_logs(self, logs: List[Dict]):
        if not logs:
            return

        existing_logs = self.read_logs()
        existing_logs.extend(logs)

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_logs, f, indent=4)
        log(f"Wrote {len(logs)} logs to JSON at {self.filepath}")

    def read_logs(self) -> List[Dict]:
        if not os.path.exists(self.filepath):
            log(f"JSON file not found at {self.filepath}", level="WARN")
            return []

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            log(f"JSON file corrupted at {self.filepath}, returning empty list", level="ERROR")
            return []

    def stream_log(self, log_entry: Dict):
        logs = self.read_logs()
        logs.append(log_entry)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=4)
        log(f"Streamed 1 log to JSON at {self.filepath}")
