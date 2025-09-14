import re
from typing import Dict, List, Optional
from datetime import datetime
from core.logger import log

class SyslogParser:
    # RFC 3164 example: "Oct 11 22:14:15 hostname appname[123]: message"
    RFC3164_REGEX = re.compile(
        r'(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+'
        r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'(?P<host>\S+)\s+'
        r'(?P<app>\S+?)(?:\[(?P<pid>\d+)\])?:\s+'
        r'(?P<message>.+)'
    )

    # RFC 5424 example: "<34>1 2025-09-14T22:14:15Z hostname appname 123 ID47 - message"
    RFC5424_REGEX = re.compile(
        r'<(?P<priority>\d+)>(?P<version>\d+) '
        r'(?P<timestamp>[\d\-T:.Z]+) '
        r'(?P<host>\S+) '
        r'(?P<app>\S+) '
        r'(?P<pid>\S+) '
        r'(?P<msgid>\S+) '
        r'(?P<structured_data>-|\[.*?\]) '
        r'(?P<message>.+)'
    )

    @staticmethod
    def parse_line(line: str) -> Optional[Dict]:
        match = SyslogParser.RFC5424_REGEX.match(line)
        if not match:
            match = SyslogParser.RFC3164_REGEX.match(line)
        if not match:
            log(f"Failed to parse syslog line: {line}", level="WARN")
            return None

        data = match.groupdict()

        # Convert timestamp if possible
        if 'timestamp' in data and data['timestamp']:
            try:
                dt = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                data['timestamp'] = dt.isoformat()
            except Exception:
                data['timestamp'] = None
        else:
            # RFC 3164: construct timestamp with current year
            try:
                current_year = datetime.utcnow().year
                dt_str = f"{data['month']} {data['day']} {current_year} {data['time']}"
                dt = datetime.strptime(dt_str, "%b %d %Y %H:%M:%S")
                data['timestamp'] = dt.isoformat()
            except Exception:
                data['timestamp'] = None

        return data

    @staticmethod
    def parse_lines(lines: List[str]) -> List[Dict]:
        parsed = []
        for line in lines:
            result = SyslogParser.parse_line(line)
            if result:
                parsed.append(result)
        log(f"Parsed {len(parsed)} syslog lines")
        return parsed
