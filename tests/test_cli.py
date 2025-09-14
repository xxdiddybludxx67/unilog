import unittest
from src.cli.ingest import Ingest
from src.cli.parse import Parse
from src.cli.tail import Tail

class TestCLI(unittest.TestCase):

    def test_ingest_reads_file(self):
        lines = Ingest.read_file("tests/sample.log")
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)

    def test_parse_auto_detect(self):
        line = "127.0.0.1 - - [14/Sep/2025:12:00:00 +0000] GET /index.html 200"
        parsed = Parse.auto_detect(line)
        self.assertIsInstance(parsed, dict)
        self.assertIn("ip", parsed)

    def test_tail_file(self):
        tail_lines = Tail.tail_file("tests/sample.log", 5)
        self.assertEqual(len(tail_lines), 5)
