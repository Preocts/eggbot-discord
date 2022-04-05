import abc
from typing import Any

from eggbot.provider.db_connector import DBConnection


class DBStoreIntfc(abc.ABC):
    """ABC for all database store providers"""

    @abc.abstractmethod
    def __init__(self, db_connection: DBConnection) -> None:
        super().__init__()
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
