from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime
from core.logger import log

class AnomalyDetector:
    def __init__(self, contamination: float = 0.01, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.model: Optional[IsolationForest] = None
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
            log("No logs provided to fit anomaly detector", level="WARN")
            return

        X = self._extract_features(logs)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
        self.model.fit(X_scaled)
        self.fitted = True
        log("Anomaly detection model fitted successfully")

    def predict(self, logs: List[Dict]) -> List[Dict]:
        if not self.fitted or not logs:
            return [{**log_entry, "anomaly": False} for log_entry in logs]

        X = self._extract_features(logs)
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)  # -1 for anomaly, 1 for normal

        for log_entry, pred in zip(logs, predictions):
            log_entry["anomaly"] = pred == -1

        return logs

    def detect_stream(self, log_stream: List[Dict]):
        detected = self.predict(log_stream)
        for entry in detected:
            if entry.get("anomaly"):
                log(f"Anomaly detected: {entry}", level="WARN")
