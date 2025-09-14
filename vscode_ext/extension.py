from src.cli.ingest import Ingest
from src.cli.parse import Parse
from src.cli.tail import Tail
from src.vscode_ext.webview import Webview
from src.vscode_ext.utils import VSUtils

class VSCodeExtension:
    def __init__(self):
        self.webview = Webview()
        self.active = False
        self.commands = {
            "unilog.ingest": self.command_ingest,
            "unilog.parse": self.command_parse,
            "unilog.tail": self.command_tail,
        }

    def activate(self):
        self.active = True
        print("[VSCodeExtension] Activated")
        self.webview.open()
        VSUtils.log_event("Extension activated")

    def deactivate(self):
        self.active = False
        print("[VSCodeExtension] Deactivated")
        VSUtils.log_event("Extension deactivated")

    def execute_command(self, command_name: str, *args, **kwargs):
        if command_name in self.commands:
            print(f"[VSCodeExtension] Executing command: {command_name}")
            return self.commands[command_name](*args, **kwargs)
        else:
            raise ValueError(f"Command '{command_name}' not found")

    def command_ingest(self, filepath: str):
        lines = Ingest.read_file(filepath)
        VSUtils.log_event(f"Ingested {len(lines)} lines from {filepath}")
        self.webview.send_message({"type": "ingest", "count": len(lines)})
        return lines

    def command_parse(self, lines):
        parsed = [Parse.auto_detect(line) for line in lines]
        VSUtils.log_event(f"Parsed {len(parsed)} lines")
        self.webview.send_message({"type": "parse", "count": len(parsed)})
        return parsed

    def command_tail(self, filepath: str, n: int = 10):
        tail_lines = Tail.tail_file(filepath, n)
        VSUtils.log_event(f"Tailed last {n} lines from {filepath}")
        self.webview.send_message({"type": "tail", "lines": tail_lines})
        return tail_lines
