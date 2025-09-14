import re
from typing import Dict, Optional
from datetime import datetime
from core.logger import log

class ApacheParser:
    # Common Log Format: 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache.gif HTTP/1.0" 200 2326
    CLF_REGEX = re.compile(
        r'(?P<ip>\S+) '           # IP address
        r'(?P<ident>\S+) '        # Identd
        r'(?P<user>\S+) '         # Authuser
        r'\[(?P<time>.*?)\] '     # Time
        r'"(?P<request>.*?)" '    # Request
        r'(?P<status>\d{3}) '     # Status code
        r'(?P<size>\S+)'          # Size
    )

    # Combined Log Format adds referer and user agent
    COMBINED_REGEX = re.compile(
        r'(?P<ip>\S+) '           
        r'(?P<ident>\S+) '
        r'(?P<user>\S+) '
        r'\[(?P<time>.*?)\] '
        r'"(?P<request>.*?)" '
        r'(?P<status>\d{3}) '
        r'(?P<size>\S+) '
        r'"(?P<referer>.*?)" '
        r'"(?P<user_agent>.*?)"'
    )

    @staticmethod
    def parse_line(line: str) -> Optional[Dict]:
        """
        Parse a single Apache log line.
        Returns a dictionary of log fields or None if it doesn't match.
        """
        match = ApacheParser.COMBINED_REGEX.match(line)
        if not match:
            match = ApacheParser.CLF_REGEX.match(line)
        if not match:
            log(f"Failed to parse line: {line}", level="WARN")
            return None

        data = match.groupdict()
        # Convert size to int, or None if '-'
        data['size'] = int(data['size']) if data['size'].isdigit() else None
        # Convert status to int
        data['status'] = int(data['status'])
        # Convert timestamp to ISO format
        try:
            data['timestamp'] = datetime.strptime(data['time'], "%d/%b/%Y:%H:%M:%S %z").isoformat()
        except Exception:
            data['timestamp'] = None
        # Split request into method, path, protocol
        try:
            method, path, protocol = data['request'].split()
            data['method'] = method
            data['path'] = path
            data['protocol'] = protocol
        except Exception:
            data['method'] = data['path'] = data['protocol'] = None

        # Remove original time and request fields
        data.pop('time', None)
        data.pop('request', None)
        return data

    @staticmethod
    def parse_lines(lines: list) -> list:
        """
        Parse multiple Apache log lines.
        Returns a list of dictionaries.
        """
        parsed = []
        for line in lines:
            result = ApacheParser.parse_line(line)
            if result:
                parsed.append(result)
        log(f"Parsed {len(parsed)} lines from Apache logs")
        return parsed
