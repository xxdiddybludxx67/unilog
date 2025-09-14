import re
from typing import Dict, List, Optional
from datetime import datetime
from core.logger import log

class GenericParser:
    def __init__(self, pattern: str = None, field_map: Dict[str, str] = None):
        self.pattern = re.compile(pattern) if pattern else None
        self.field_map = field_map or {}

    def parse_line(self, line: str) -> Optional[Dict]:
        data = {}

        if self.pattern:
            match = self.pattern.match(line)
            if match:
                data = match.groupdict()
        else:
            # Fallback: key=value pairs
            try:
                for part in line.strip().split():
                    if "=" in part:
                        key, value = part.split("=", 1)
                        data[key] = value
            except Exception:
                log(f"Failed fallback parsing for line: {line}", level="WARN")
                return None

        if not data:
            log(f"Line did not match any parsing strategy: {line}", level="WARN")
            return None

        # Apply field map renaming
        for key, new_key in self.field_map.items():
            if key in data:
                data[new_key] = data.pop(key)

        # Attempt to parse timestamps if present
        if "timestamp" in data:
            try:
                dt = datetime.fromisoformat(data["timestamp"])
                data["timestamp"] = dt.isoformat()
            except Exception:
                pass

        return data

    def parse_lines(self, lines: List[str]) -> List[Dict]:
        parsed = []
        for line in lines:
            result = self.parse_line(line)
            if result:
                parsed.append(result)
        log(f"Parsed {len(parsed)} lines using GenericParser")
        return parsed
