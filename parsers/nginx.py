import re
from typing import Dict, List, Optional
from datetime import datetime
from core.logger import log

class NginxParser:
    # Default combined log format regex
    COMBINED_REGEX = re.compile(
        r'(?P<ip>\S+) '                 # IP address
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
        match = NginxParser.COMBINED_REGEX.match(line)
        if not match:
            from core.logger import LogLevel
            log(f"Failed to parse Nginx line: {line}", level=LogLevel.WARNING)
            return None

        data = match.groupdict()
        # Convert numeric fields
        data['status'] = int(data['status'])
        data['size'] = int(data['size']) if data['size'].isdigit() else None

        # Convert timestamp
        try:
            data['timestamp'] = datetime.strptime(data['time'], "%d/%b/%Y:%H:%M:%S %z").isoformat()
        except Exception:
            data['timestamp'] = None

        # Split request
        try:
            method, path, protocol = data['request'].split()
            data['method'] = method
            data['path'] = path
            data['protocol'] = protocol
        except Exception:
            data['method'] = data['path'] = data['protocol'] = None

        # Remove original fields
        data.pop('time', None)
        data.pop('request', None)
        return data

    @staticmethod
    def parse_lines(lines: List[str]) -> List[Dict]:
        parsed = []
        for line in lines:
            result = NginxParser.parse_line(line)
            if result:
                parsed.append(result)
        log(f"Parsed {len(parsed)} Nginx lines")
        return parsed
