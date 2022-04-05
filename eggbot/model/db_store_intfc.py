import abc
from typing import Any


class DBStoreIntfc(abc.ABC):
    """ABC for all database store providers"""

    # @abc.abstractmethod
    # def save(self) -> None:
    #     """Override for database specific save method"""
    #     raise NotImplementedError()

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
