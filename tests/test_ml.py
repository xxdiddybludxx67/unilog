import unittest
from ml.anomaly_detection import AnomalyDetector
from ml.clustering import LogClustering

class TestML(unittest.TestCase):
    def setUp(self):
        self.logs = [
            {"timestamp": "2025-09-15T12:00:00", "level": "INFO", "message": "ok"},
            {"timestamp": "2025-09-15T12:01:00", "level": "INFO", "message": "ok"},
            {"timestamp": "2025-09-15T12:02:00", "level": "ERROR", "message": "fail"},
            {"timestamp": "2025-09-15T12:03:00", "level": "INFO", "message": "ok"},
            {"timestamp": "2025-09-15T12:04:00", "level": "INFO", "message": "ok"},
        ]

    def test_anomaly_detector(self):
        detector = AnomalyDetector()
        detector.fit(self.logs)
        results = detector.predict(self.logs)
        self.assertEqual(len(results), len(self.logs))
        self.assertIn("anomaly", results[0])

    def test_log_clustering(self):
        clustering = LogClustering(n_clusters=2)
        clustering.fit(self.logs)
        results = clustering.predict(self.logs)
        self.assertEqual(len(results), len(self.logs))
        self.assertIn("cluster", results[0])
