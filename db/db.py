import psycopg2
from psycopg2.errors import UniqueViolation
import os
from typing import Optional, Tuple


class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            config = {
                "dbname": os.environ.get("DB_NAME"),
                "user": os.environ.get("DB_USER"),
                "password": os.environ.get("DB_PASSWORD"),
                "host": os.environ.get("DB_HOST"),
                "port": os.environ.get("DB_PORT")
            }
            cls._instance._conn = psycopg2.connect(**config)
        return cls._instance

    def execute(self, query: str, values: Optional[Tuple] = None):
        try:
            with self._instance._conn:
                c = self._conn.cursor()
                if values:
                    c.execute(query, values)
                    self._conn.commit()
                else:
                    c.execute(query)
            self._instance._conn.close()
        except UniqueViolation:
            print("Ignorando arquivo duplicado")
