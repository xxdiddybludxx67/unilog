import sqlite3
from sqlite3 import Connection, Cursor
from typing import List, Dict
from datetime import datetime
from core.logger import log
import json

class SQLiteDB:
    def __init__(self, db_path: str = "unilog.db"):
        self.db_path = db_path
        self.conn: Connection = None
        self.cursor: Cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            log(f"Connected to SQLite at {self.db_path}")
        except Exception as e:
            log(f"Failed to connect to SQLite: {e}", level="ERROR")
            raise

    def create_table(self, table_name: str = "logs"):
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT,
            message TEXT,
            data TEXT
        );
        """
        self.cursor.execute(query)
        self.conn.commit()
        log(f"Table '{table_name}' ensured in SQLite")

    def insert_logs(self, logs: List[Dict], table_name: str = "logs"):
        if not logs:
            return

        query = f"INSERT INTO {table_name} (timestamp, level, message, data) VALUES (?, ?, ?, ?);"

        formatted_logs = []
        for log_entry in logs:
            formatted_logs.append((
                log_entry.get("timestamp", datetime.utcnow().isoformat()),
                log_entry.get("level", "INFO"),
                log_entry.get("message", ""),
                json.dumps({k: v for k, v in log_entry.items() if k not in ["timestamp", "level", "message"]})
            ))

        try:
            self.cursor.executemany(query, formatted_logs)
            self.conn.commit()
            log(f"Inserted {len(formatted_logs)} logs into SQLite")
        except Exception as e:
            self.conn.rollback()
            log(f"Failed to insert logs into SQLite: {e}", level="ERROR")

    def fetch_logs(self, limit: int = 100, table_name: str = "logs") -> List[Dict]:
        query = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT ?;"
        self.cursor.execute(query, (limit,))
        rows = self.cursor.fetchall()
        results = []
        for row in rows:
            data = json.loads(row["data"]) if row["data"] else {}
            results.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "level": row["level"],
                "message": row["message"],
                **data
            })
        return results

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            log("SQLite connection closed")
