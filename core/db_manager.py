import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from core.logger import log

# Default configuration for DB
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/unilog.db")
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "dbname": os.getenv("POSTGRES_DB", "unilog"),
}


class DBManager:
    def __init__(self, db_type: str = "sqlite"):
        self.db_type = db_type.lower()
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            if self.db_type == "sqlite":
                self.conn = sqlite3.connect(SQLITE_DB_PATH)
                self.cursor = self.conn.cursor()
                log(f"Connected to SQLite at {SQLITE_DB_PATH}")
            elif self.db_type == "postgres":
                self.conn = psycopg2.connect(**POSTGRES_CONFIG, cursor_factory=RealDictCursor)
                self.cursor = self.conn.cursor()
                log(f"Connected to PostgreSQL at {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
            else:
                raise ValueError(f"Unsupported DB type: {self.db_type}")
        except Exception as e:
            log(f"Database connection failed: {e}")
            raise

    def execute(self, query: str, params=None):
        try:
            if params is None:
                params = ()
            self.cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                result = self.cursor.fetchall()
                return result
            else:
                self.conn.commit()
        except Exception as e:
            log(f"Query failed: {query} | Exception: {e}")
            raise

    def insert(self, table: str, data: dict):
        keys = ", ".join(data.keys())
        values = tuple(data.values())
        placeholders = ", ".join(["%s"] * len(data)) if self.db_type == "postgres" else ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        self.execute(query, values)

    def fetch_all(self, table: str, limit: int = 100):
        query = f"SELECT * FROM {table} LIMIT {limit}"
        return self.execute(query)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        log(f"Closed {self.db_type} database connection")
