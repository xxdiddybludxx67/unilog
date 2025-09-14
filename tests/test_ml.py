import unittest
from src.ml.anomalyDetection import AnomalyDetection
from src.ml.clustering import Clustering

class TestML(unittest.TestCase):

    def test_anomaly_detection(self):
        data = [1, 2, 1, 2, 100]
        anomalies = AnomalyDetection.detect(data)
        self.assertIn(100, anomalies)

    def test_clustering(self):
        points = [[1, 2], [2, 3], [100, 100]]
        clusters = Clustering.kmeans(points, k=2)
        self.assertEqual(len(clusters), 2)
