import unittest
from src.outputs.csv_output import CSVOutput
from src.outputs.json_output import JSONOutput

class TestOutputs(unittest.TestCase):

    def test_csv_output(self):
        data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        filepath = "tests/test.csv"
        CSVOutput.write(data, filepath)
        with open(filepath, "r") as f:
            lines = f.readlines()
        self.assertGreater(len(lines), 0)

    def test_json_output(self):
        data = {"event": "login", "user": "bob"}
        filepath = "tests/test.json"
        JSONOutput.write(data, filepath)
        with open(filepath, "r") as f:
            content = f.read()
        self.assertIn("bob", content)
