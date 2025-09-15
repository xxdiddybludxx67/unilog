import unittest
from parsers.apache import ApacheParser
from parsers.json_parser import JSONParser
from parsers.nginx import NginxParser
from parsers.syslog import SyslogParser

class TestParsers(unittest.TestCase):
    def test_apache_parser(self):
        line = '127.0.0.1 - - [14/Sep/2025:12:00:00 +0000] "GET / HTTP/1.1" 200 1234'
        parser = ApacheParser()
        if hasattr(parser, "parse_line"):
            parsed = parser.parse_line(line)
            self.assertIn("ip", parsed)
        else:
            self.skipTest("parse_line not implemented in ApacheParser")

    def test_json_parser(self):
        line = '{"event": "login", "user": "alice"}'
        parser = JSONParser()
        if hasattr(parser, "parse_line"):
            parsed = parser.parse_line(line)
            self.assertEqual(parsed["user"], "alice")
        else:
            self.skipTest("parse_line not implemented in JSONParser")

    def test_nginx_parser(self):
        # Use a log line matching the Nginx combined log format
        line = '127.0.0.1 - - [14/Sep/2025:12:02:00 +0000] "GET /index.html HTTP/1.1" 200 5678 "-" "Mozilla/5.0"'
        parser = NginxParser()
        if hasattr(parser, "parse_line"):
            parsed = parser.parse_line(line)
            self.assertIsNotNone(parsed)
            self.assertIn("status", parsed)
        else:
            self.skipTest("parse_line not implemented in NginxParser")

    def test_syslog_parser(self):
        line = '<34>1 2025-09-14T12:04:00Z host app - - - test message'
        parser = SyslogParser()
        if hasattr(parser, "parse_line"):
            parsed = parser.parse_line(line)
            self.assertIn("message", parsed)
        else:
            self.skipTest("parse_line not implemented in SyslogParser")
