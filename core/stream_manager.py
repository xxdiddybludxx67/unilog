import threading
import queue
from typing import Callable, List, Dict, Optional
from core.logger import log
from core.parser_manager import ParserManager
from core.filter import apply_filter
from core.output_manager import OutputManager

class StreamManager:
    def __init__(
        self,
        parser_manager: Optional[ParserManager] = None,
        output_manager: Optional[OutputManager] = None,
        filters: Optional[List[Dict]] = None,
        num_worker_threads: int = 4,
    ):
        self.parser_manager = parser_manager or ParserManager()
        self.output_manager = output_manager or OutputManager()
        self.filters = filters or []
        self.queue = queue.Queue()
        self.num_worker_threads = num_worker_threads
        self.workers = []
        self.running = False

    def enqueue(self, log_type: str, line: str):
        self.queue.put((log_type, line))

    def _worker(self):
        while self.running:
            try:
                log_type, line = self.queue.get(timeout=1)
            except queue.Empty:
                continue

            # Parse
            parsed = self.parser_manager.parse(log_type, line)
            if not parsed:
                self.queue.task_done()
                continue

            # Filter
            filtered = apply_filter(parsed, self.filters)
            if not filtered:
                self.queue.task_done()
                continue

            # Output
            self.output_manager.write([filtered])
            self.queue.task_done()

    def start(self):
        self.running = True
        for _ in range(self.num_worker_threads):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            self.workers.append(t)
        log(f"Started {self.num_worker_threads} worker threads for streaming.")

    def stop(self):
        self.running = False
        for t in self.workers:
            t.join(timeout=2)
        log("Stopped all worker threads for streaming.")

    def wait_for_completion(self):
        self.queue.join()
