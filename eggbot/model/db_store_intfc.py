from __future__ import annotations

import abc
from contextlib import contextmanager
from typing import Any
from typing import Generator

from eggbot.provider.db_connector import Cursor
from eggbot.provider.db_connector import DBConnection


class DBStoreIntfc(abc.ABC):
    """ABC for all database store providers"""

    # Reusable code
    @contextmanager
    def get_cursor(self) -> Generator[Cursor, None, None]:
        """Context manager for creating a database cursor. Does not commit changes."""
        cursor = self.dbconn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    # Override the following methods for each implementation
    @abc.abstractmethod
    def __init__(self, db_connection: DBConnection) -> None:
        self.dbconn = db_connection  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self) -> list[Any]:
        """Override for database specific get method"""
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, event: str) -> None:
        """Override for database specific save method"""
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, uid: str) -> None:
        """Override for database specific delete method"""
        raise NotImplementedError()

    @abc.abstractmethod
    def _to_model(self, row: list[list[Any]]) -> list[Any]:
        """Override to model database rows to object"""
        raise NotImplementedError()
