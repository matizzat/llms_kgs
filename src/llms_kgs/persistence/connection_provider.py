from psycopg2.extensions import connection as PgConnection
from pgvector.psycopg2 import register_vector
from .database_error import DatabaseError
from llms_kgs.core_utils import log_error
import psycopg2

class ConnectionProvider:
    def __init__(self, dbname: str, port: str, host: str, user: str,
                 password: str | None = None):
        self._dbname = dbname
        self._host = host
        self._user = user
        self._port = port
        self._password = password
        self._conn: PgConnection | None = None

    def _connect(self) -> PgConnection:
        conn = psycopg2.connect(
            dbname=self._dbname,
            port=self._port,
            host=self._host,
            user=self._user,
            password=self._password,
            connect_timeout=5
        )
        register_vector(conn)
        return conn

    def _handle_exception(self, method_name: str, e: Exception):
        log_error('ConnectionProvider', method_name, e)
        raise DatabaseError(f"{method_name} failed: {e}") from e

    def get_connection(self) -> PgConnection:
        try:
            if (
                self._conn is None or
                self._conn.closed or
                self._conn.status != psycopg2.extensions.STATUS_READY
            ):
                self._conn = self._connect()
            return self._conn
        except Exception as e:
            self._handle_exception('get_connection', e)

    def close_connection(self):
        try:
            if self._conn and not self._conn.closed:
                self._conn.close()
        except Exception as e:
            self._handle_exception('close_connection', e)

    def __enter__(self) -> PgConnection:
        return self.get_connection()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
