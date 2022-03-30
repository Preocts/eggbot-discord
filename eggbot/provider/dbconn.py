from __future__ import annotations

import contextlib
import sqlite3
from typing import Generator


class DBConn:
    def __init__(
        self,
        url: str | None = None,
        user: str | None = None,
        password: str | None = None,
        port: int | None = None,
    ) -> None:
        """
        Prepare a connection to the database with optional requirements.

        Args:
            url: URL to database
            user: Username to login to database
            password: Password to login to database
            port: Port open to database traffic
        """
        self.url = url
        self.user = user
        self.password = password
        self.port = port
        self._active: dict[str, sqlite3.Connection] = {}

    @contextlib.contextmanager
    def get_connection(
        self,
        database_name: str,
    ) -> Generator[sqlite3.Connection, None, None]:
        """
        Open a connection to the given database.

        Args:
            database_name: Name of database to open

        Yields:
            SQL Database connection.
        """
        if database_name not in self._active:
            self._active[database_name] = sqlite3.connect(database_name)

        try:
            yield self._active[database_name]
        finally:
            self._active[database_name].close()
            self._active.pop(database_name, None)
