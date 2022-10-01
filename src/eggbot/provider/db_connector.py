from __future__ import annotations

import contextlib
import dataclasses
import sqlite3
from typing import Generator

# Explict type alias definitions for abstract from DB engine
# Cannot be class-level until 3.10
Cursor = sqlite3.Cursor
IntegrityError = sqlite3.IntegrityError


@dataclasses.dataclass
class _ActiveConnections:
    connection: sqlite3.Connection
    count: int


class DBConnection:
    """Database connection abstract. Use this over importing DB library"""

    def __init__(self, dbconn: sqlite3.Connection) -> None:
        self._dbconn = dbconn

    def cursor(self) -> sqlite3.Cursor:
        """Create a database cursor"""
        return self._dbconn.cursor()

    def commit(self) -> None:
        """Commit pending changes to database"""
        return self._dbconn.commit()

    def close(self) -> None:
        """Close database connection. Use with care, allow context to handle."""
        return self._dbconn.close()


class DBConnector:
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
        self._active: dict[str, _ActiveConnections] = {}

    @contextlib.contextmanager
    def get_connection(
        self,
        database_name: str,
    ) -> Generator[DBConnection, None, None]:
        """
        Open a connection to the given database.

        Args:
            database_name: Name of database to open

        Yields:
            SQL Database connection.
        """
        if database_name not in self._active:
            self._active[database_name] = _ActiveConnections(
                connection=sqlite3.connect(database_name),
                count=1,
            )
        else:
            self._active[database_name].count += 1

        try:
            yield DBConnection(self._active[database_name].connection)

        finally:
            self._active[database_name].count -= 1
            if not self._active[database_name].count:
                self._active[database_name].connection.close()
                self._active.pop(database_name, None)
