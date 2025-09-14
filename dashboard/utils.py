from typing import List, Dict
from datetime import datetime
from core.stream_manager import StreamManager
from core.parser_manager import ParserManager
from core.filter import apply_filter
from core.output_manager import OutputManager

stream_manager = StreamManager()
parser_manager = ParserManager()
output_manager = OutputManager()


def fetch_logs(limit: int = 100) -> List[Dict]:
    recent_logs = []
    try:
        queue_copy = list(stream_manager.queue.queue)
        for log_type, line in queue_copy[-limit:]:
            parsed = parser_manager.parse(log_type, line)
            filtered = apply_filter(parsed, [])
            if filtered:
                recent_logs.append(filtered)
    except Exception as e:
        print(f"Failed to fetch logs: {e}")
    return recent_logs


def format_log_entry(log_entry: Dict) -> Dict:
    return {
        "timestamp": log_entry.get("timestamp") or datetime.utcnow().isoformat(),
        "level": log_entry.get("level", "INFO"),
        "message": log_entry.get("message", ""),
        **log_entry  # Include any additional fields
    }


def push_log_to_dashboard(log_entry: Dict):
    formatted = format_log_entry(log_entry)
    from dashboard.index import push_log  # Import here to avoid circular imports
    push_log(formatted)


def send_logs_to_outputs(log_entry: Dict):
    output_manager.write([log_entry])
