import datetime
import json
import os

class VSUtils:
    LOG_FILE = "vscode_extension.log"

    @staticmethod
    def log_event(message: str):
        timestamp = datetime.datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)  # Also print to console
        with open(VSUtils.LOG_FILE, "a") as f:
            f.write(log_entry + "\n")

    @staticmethod
    def safe_write_json(filepath: str, data):
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            VSUtils.log_event(f"Written JSON to {filepath}")
        except Exception as e:
            VSUtils.log_event(f"Error writing JSON to {filepath}: {e}")
            raise

    @staticmethod
    def safe_delete_file(filepath: str):
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                VSUtils.log_event(f"Deleted file {filepath}")
            except Exception as e:
                VSUtils.log_event(f"Error deleting file {filepath}: {e}")
                raise

    @staticmethod
    def format_message(msg_type: str, content):
        return {"type": msg_type, "content": content}
