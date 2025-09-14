from elasticsearch import Elasticsearch, helpers
from typing import List, Dict
from core.logger import log
from datetime import datetime

class ElasticOutput:
    def __init__(self, hosts: List[str] = None, index_name: str = None):
        self.hosts = hosts or ["http://localhost:9200"]
        self.index_name = index_name or f"logs-{datetime.utcnow().strftime('%Y.%m.%d')}"
        self.client = Elasticsearch(hosts=self.hosts)
        self._ensure_index()

    def _ensure_index(self):
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name)
            log(f"Elasticsearch index created: {self.index_name}")

    def write_logs(self, logs: List[Dict]):
        if not logs:
            return

        actions = []
        for log_entry in logs:
            doc = {
                "_index": self.index_name,
                "_source": {
                    "timestamp": log_entry.get("timestamp", datetime.utcnow().isoformat()),
                    "level": log_entry.get("level", "INFO"),
                    "message": log_entry.get("message", ""),
                    **{k: v for k, v in log_entry.items() if k not in ["timestamp", "level", "message"]}
                }
            }
            actions.append(doc)

        try:
            helpers.bulk(self.client, actions)
            log(f"Bulk indexed {len(logs)} logs to Elasticsearch index {self.index_name}")
        except Exception as e:
            log(f"Error writing logs to Elasticsearch: {e}", level="ERROR")

    def stream_log(self, log_entry: Dict):
        self.write_logs([log_entry])

    def search_logs(self, query: Dict = None, size: int = 1000) -> List[Dict]:
        query = query or {"query": {"match_all": {}}}
        try:
            response = self.client.search(index=self.index_name, body=query, size=size)
            hits = response.get("hits", {}).get("hits", [])
            return [hit["_source"] for hit in hits]
        except Exception as e:
            log(f"Error searching logs in Elasticsearch: {e}", level="ERROR")
            return []
