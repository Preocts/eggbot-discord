from __future__ import annotations

import datetime
from typing import Any
from uuid import uuid4

from eggbot.model.db_store_intfc import DBStoreIntfc
from eggbot.model.deferred_task import DeferredTask
from eggbot.provider.db_connector import DBConnection


class DeferredTaskDB(DBStoreIntfc):
    def __init__(self, db_connection: DBConnection) -> None:
        """CRUD method layer for Deferred Task table"""
        self.dbconn = db_connection

        self._init_table()

    def _init_table(self) -> None:
        """Build table if needed"""
        sql = (
            "CREATE TABLE IF NOT EXISTS deferred_task (uid TEXT PRIMARY KEY, "
            "created_at TEXT, retry_at TEXT, event_type TEXT, "
            "event TEXT, attempts INT)"
        )
        with self.get_cursor() as cursor:
            cursor.execute(sql)
            self.dbconn.commit()

    def row_count(self) -> int:
        """Return total rows in deferred task table"""
        sql = "SELECT COUNT(uid) FROM deferred_task"
        with self.get_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]

    def save(self, event: str, type_: str = "default", retry_after: int = 0) -> None:
        """
        Save deferred task to database.

        Args:
            event: Serialized event payload to event handlers
            type_: Optional type classification of event
            retry_after: Number of seconds to wait, from save, before retry is attempted

            NOTE: retry_after only affects the first retry attempt

        Returns:
            None
        """
        now = datetime.datetime.utcnow()
        after = now + datetime.timedelta(seconds=retry_after)
        sql = (
            "INSERT INTO deferred_task (uid, created_at, retry_at, event_type, event, "
            "attempts) VALUES (?, ?, ?, ?, ?, ?)"
        )

        with self.get_cursor() as cursor:
            cursor.execute(sql, (str(uuid4()), now, after, type_, event, 0))
            self.dbconn.commit()

    def get(self, event_type: str | None = None) -> list[DeferredTask]:
        """
        Return deferred tasks from database

        Args:
            event_type: Optional filter by event type otherwise return all
        """
        if event_type:
            sql = "SELECT * FROM deferred_task WHERE event_type=?"
            values = [event_type]
        else:
            sql = "SELECT * FROM deferred_task"
            values = []

        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            return self._to_model(cursor.fetchall())

    def delete(self, uid: str) -> None:
        """
        Delete row from deferred_task table by uid

        Args:
            uid: UID of row to delete

        Returns:
            None
        """
        sql = "DELETE FROM deferred_task WHERE uid=?"
        with self.get_cursor() as cursor:
            cursor.execute(sql, (uid,))
            self.dbconn.commit()

    def _to_model(self, rows: list[list[Any]]) -> list[DeferredTask]:
        """Convert rows into DeferredTask model."""
        return [DeferredTask(*row) for row in rows]
