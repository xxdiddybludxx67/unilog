import unittest
from cli import utils
from cli import tail

class TestCLI(unittest.TestCase):
    def test_read_file(self):
        lines = utils.read_file("tests/sample.log")
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)

    def test_tail_file(self):
        # tail_file is a method, not static, so instantiate Tail
        if hasattr(tail, "Tail"):
            t = tail.Tail()
            result = t.tail_file("tests/sample.log")
            self.assertIsInstance(result, list)
        else:
            self.skipTest("Tail class not implemented")
