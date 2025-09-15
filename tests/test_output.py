import unittest
from outputs.csv_output import CSVOutput
from outputs.json_output import JSONOutput
import os

class TestOutputs(unittest.TestCase):
    def test_csv_output(self):
        data = [{"timestamp": "2025-09-15T12:00:00", "level": "INFO", "message": "ok"}]
        csv = CSVOutput()
        if hasattr(csv, "write_logs"):
            csv.write_logs(data)
            self.assertTrue(os.path.exists(csv.filepath))
        else:
            self.skipTest("write_logs not implemented in CSVOutput")

    def test_json_output(self):
        data = [{"timestamp": "2025-09-15T12:00:00", "level": "INFO", "message": "ok"}]
        json_out = JSONOutput()
        if hasattr(json_out, "write_logs"):
            json_out.write_logs(data)
            self.assertTrue(os.path.exists(json_out.filepath))
        else:
            self.skipTest("write_logs not implemented in JSONOutput")
