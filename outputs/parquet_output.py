import os
from typing import List, Dict
from datetime import datetime
import pandas as pd
from core.logger import log

class ParquetOutput:
    def __init__(self, output_dir: str = "logs/parquet", filename: str = None):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.filename = filename or f"logs_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.parquet"
        self.filepath = os.path.join(self.output_dir, self.filename)
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            df = pd.DataFrame(columns=["timestamp", "level", "message", "data"])
            df.to_parquet(self.filepath, engine="pyarrow", index=False)
            log(f"Parquet file created at {self.filepath}")

    def write_logs(self, logs: List[Dict]):
        if not logs:
            return

        try:
            if os.path.exists(self.filepath):
                existing_df = pd.read_parquet(self.filepath, engine="pyarrow")
                new_df = pd.DataFrame([{
                    "timestamp": log.get("timestamp", datetime.utcnow().isoformat()),
                    "level": log.get("level", "INFO"),
                    "message": log.get("message", ""),
                    "data": {k: v for k, v in log.items() if k not in ["timestamp", "level", "message"]}
                } for log in logs])
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                combined_df = pd.DataFrame([{
                    "timestamp": log.get("timestamp", datetime.utcnow().isoformat()),
                    "level": log.get("level", "INFO"),
                    "message": log.get("message", ""),
                    "data": {k: v for k, v in log.items() if k not in ["timestamp", "level", "message"]}
                } for log in logs])

            combined_df.to_parquet(self.filepath, engine="pyarrow", index=False)
            log(f"Wrote {len(logs)} logs to Parquet at {self.filepath}")
        except Exception as e:
            log(f"Error writing logs to Parquet: {e}", level="ERROR")

    def read_logs(self) -> List[Dict]:
        if not os.path.exists(self.filepath):
            log(f"Parquet file not found at {self.filepath}", level="WARN")
            return []

        try:
            df = pd.read_parquet(self.filepath, engine="pyarrow")
            logs = []
            for _, row in df.iterrows():
                log_entry = {
                    "timestamp": row.get("timestamp"),
                    "level": row.get("level"),
                    "message": row.get("message"),
                }
                log_entry.update(row.get("data", {}))
                logs.append(log_entry)
            return logs
        except Exception as e:
            log(f"Error reading logs from Parquet: {e}", level="ERROR")
            return []

    def stream_log(self, log_entry: Dict):
        self.write_logs([log_entry])
