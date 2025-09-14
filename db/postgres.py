import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
from typing import List, Dict
from core.logger import log

class PostgresDB:
    def __init__(self, host: str = "localhost", port: int = 5432, dbname: str = "unilog",
                 user: str = "postgres", password: str = "postgres"):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password
        }
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            log("Connected to PostgreSQL")
        except Exception as e:
            log(f"Failed to connect to PostgreSQL: {e}", level="ERROR")
            raise

    def create_table(self, table_name: str = "logs"):
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            level VARCHAR(20),
            message TEXT,
            data JSONB
        );
        """
        self.cursor.execute(query)
        self.conn.commit()
        log(f"Table '{table_name}' ensured in PostgreSQL")

    def insert_logs(self, logs: List[Dict], table_name: str = "logs"):
        if not logs:
            return

        query = f"""
        INSERT INTO {table_name} (timestamp, level, message, data)
        VALUES (%(timestamp)s, %(level)s, %(message)s, %(data)s);
        """

        # Ensure 'data' field contains all extra fields
        formatted_logs = []
        for log_entry in logs:
            formatted_logs.append({
                "timestamp": log_entry.get("timestamp"),
                "level": log_entry.get("level", "INFO"),
                "message": log_entry.get("message", ""),
                "data": {k: v for k, v in log_entry.items() if k not in ["timestamp", "level", "message"]}
            })

        try:
            execute_batch(self.cursor, query, formatted_logs)
            self.conn.commit()
            log(f"Inserted {len(formatted_logs)} logs into PostgreSQL")
        except Exception as e:
            self.conn.rollback()
            log(f"Failed to insert logs into PostgreSQL: {e}", level="ERROR")

    def fetch_logs(self, limit: int = 100, table_name: str = "logs") -> List[Dict]:
        query = f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT %s;"
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            log("PostgreSQL connection closed")
