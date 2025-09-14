from typing import List, Dict
from datetime import datetime
import numpy as np

LEVEL_MAP = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "CRITICAL": 4}


def standardize_logs(logs: List[Dict]) -> List[Dict]:
    standardized = []
    for log_entry in logs:
        standardized.append({
            "timestamp": log_entry.get("timestamp", datetime.utcnow().isoformat()),
            "level": log_entry.get("level", "INFO"),
            "message": log_entry.get("message", ""),
            **{k: v for k, v in log_entry.items() if k not in ["timestamp", "level", "message"]}
        })
    return standardized


def extract_features(logs: List[Dict]) -> np.ndarray:
    features = []
    last_ts = None
    for log_entry in logs:
        msg_len = len(log_entry.get("message", ""))
        level = LEVEL_MAP.get(log_entry.get("level", "INFO"), 1)
        ts = log_entry.get("timestamp")
        ts_delta = 0
        if ts:
            ts_obj = datetime.fromisoformat(ts)
            if last_ts:
                ts_delta = (ts_obj - last_ts).total_seconds()
            last_ts = ts_obj
        features.append([msg_len, level, ts_delta])
    return np.array(features)


def summarize_clusters(logs: List[Dict], cluster_field: str = "cluster") -> Dict[int, int]:
    summary = {}
    for log_entry in logs:
        cluster = log_entry.get(cluster_field)
        if cluster is not None:
            summary[cluster] = summary.get(cluster, 0) + 1
    return summary


def filter_anomalies(logs: List[Dict], anomaly_field: str = "anomaly") -> List[Dict]:
    return [log_entry for log_entry in logs if log_entry.get(anomaly_field, False)]


def top_messages(logs: List[Dict], top_n: int = 5) -> Dict[str, int]:
    counter = {}
    for log_entry in logs:
        msg = log_entry.get("message", "")
        counter[msg] = counter.get(msg, 0) + 1
    sorted_msgs = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    return dict(list(sorted_msgs.items())[:top_n])
