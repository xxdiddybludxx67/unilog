import unittest
from src.parsers.apache import ApacheParser
from src.parsers.json_parser import JSONParser
from src.parsers.nginx import NginxParser
from src.parsers.syslog import SyslogParser

class TestParsers(unittest.TestCase):

    def test_apache_parser(self):
        line = '127.0.0.1 - - [14/Sep/2025:12:00:00 +0000] "GET / HTTP/1.1" 200 1234'
        parsed = ApacheParser.parse(line)
        self.assertIn("ip", parsed)

    def test_json_parser(self):
        line = '{"event": "login", "user": "alice"}'
        parsed = JSONParser.parse(line)
        self.assertEqual(parsed["user"], "alice")

    def test_nginx_parser(self):
        line = '127.0.0.1 - - [14/Sep/2025:12:02:00 +0000] "GET / HTTP/1.1" 200 5678'
        parsed = NginxParser.parse(line)
        self.assertIn("status", parsed)

    def test_syslog_parser(self):
        line = '<34>1 2025-09-14T12:04:00Z host app - - - test message'
        parsed = SyslogParser.parse(line)
        self.assertIn("message", parsed)
