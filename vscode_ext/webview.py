from src.vscode_ext.utils import VSUtils

class Webview:
    def __init__(self):
        self.is_open = False
        self.message_queue = []

    def open(self):
        self.is_open = True
        VSUtils.log_event("[Webview] Opened webview")

    def close(self):
        self.is_open = False
        VSUtils.log_event("[Webview] Closed webview")

    def send_message(self, message: dict):
        if not self.is_open:
            VSUtils.log_event("[Webview] Attempted to send message while closed")
            return
        formatted = VSUtils.format_message(message.get("type", "unknown"), message.get("content", message))
        self.message_queue.append(formatted)
        VSUtils.log_event(f"[Webview] Sent message: {formatted}")

    def receive_message(self):
        if not self.message_queue:
            return None
        message = self.message_queue.pop(0)
        VSUtils.log_event(f"[Webview] Received message: {message}")
        return message

    def clear_queue(self):
        self.message_queue = []
        VSUtils.log_event("[Webview] Cleared message queue")
