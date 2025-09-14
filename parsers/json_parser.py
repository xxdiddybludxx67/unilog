import json
from typing import Dict, List, Optional
from core.logger import log
from datetime import datetime

class JSONParser:
    @staticmethod
    def parse_line(line: str) -> Optional[Dict]:
        try:
            data = json.loads(line)
            # Normalize timestamp if exists
            if "timestamp" in data:
                try:
                    dt = datetime.fromisoformat(data["timestamp"])
                    data["timestamp"] = dt.isoformat()
                except Exception:
                    pass
            return data
        except json.JSONDecodeError:
            log(f"Failed to parse JSON line: {line}", level="WARN")
            return None

    @staticmethod
    def parse_lines(lines: List[str]) -> List[Dict]:
        parsed = []
        for line in lines:
            result = JSONParser.parse_line(line)
            if result:
                parsed.append(result)
        log(f"Parsed {len(parsed)} JSON lines")
        return parsed
