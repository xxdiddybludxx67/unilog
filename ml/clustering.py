from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime
from core.logger import log

class LogClustering:
    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model: Optional[KMeans] = None
        self.scaler: Optional[StandardScaler] = None
        self.fitted = False

    def _extract_features(self, logs: List[Dict]) -> np.ndarray:
        features = []
        last_ts = None
        level_map = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "CRITICAL": 4}

        for log_entry in logs:
            message_len = len(log_entry.get("message", ""))
            level = level_map.get(log_entry.get("level", "INFO"), 1)
            ts = log_entry.get("timestamp")
            ts_delta = 0
            if ts:
                ts_obj = datetime.fromisoformat(ts)
                if last_ts:
                    ts_delta = (ts_obj - last_ts).total_seconds()
                last_ts = ts_obj
            features.append([message_len, level, ts_delta])

        return np.array(features)

    def fit(self, logs: List[Dict]):
        if not logs:
            log("No logs provided to fit clustering model", level="WARN")
            return

        X = self._extract_features(logs)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)
        self.model.fit(X_scaled)
        self.fitted = True
        log(f"Clustering model fitted with {self.n_clusters} clusters")

    def predict(self, logs: List[Dict]) -> List[Dict]:
        if not self.fitted or not logs:
            return [{**log_entry, "cluster": None} for log_entry in logs]

        X = self._extract_features(logs)
        X_scaled = self.scaler.transform(X)
        labels = self.model.predict(X_scaled)

        for log_entry, label in zip(logs, labels):
            log_entry["cluster"] = int(label)

        return logs

    def cluster_stream(self, log_stream: List[Dict]):
        clustered_logs = self.predict(log_stream)
        for entry in clustered_logs:
            # Here you could push cluster info to dashboard or output manager
            log(f"Log assigned to cluster {entry['cluster']}: {entry['message']}")
