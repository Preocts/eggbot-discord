from __future__ import annotations

import datetime
import json
from typing import Any
from uuid import uuid4

from eggbot.model.db_store_intfc import DBStoreIntfc
from eggbot.model.deferred_task import DeferredTask
from eggbot.provider.db_connector import DBConnection


class DeferredTaskDB(DBStoreIntfc):

    IntegrityError = DBConnection.IntegrityError

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
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql)
            self.dbconn.commit()
        finally:
            cursor.close()

    def row_count(self) -> int:
        """Return total rows in deferred task table"""
        sql = "SELECT COUNT(uid) FROM deferred_task"
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def save(self, event: dict[str, Any], retry_after: int = 0) -> None:
        """
        Save deferred task to database.

        Args:
            event: Deliverable event payload to event handlers
            retry_after: Number of seconds to wait, from save, before retry is attempted

            NOTE: retry_after only affects the first retry attempt
            NOTE: `uid` within the event is used as a unique key. If missing
                    a uuid is generated.

        Returns:
            None

        Raises:
            KeyError: Missing `event_type` key in event
            DeferredTask.IntegrityError: Non-unique `uid` provided in event
        """
        now = datetime.datetime.utcnow()
        after = now + datetime.timedelta(seconds=retry_after)
        uid = event.get("uid") or str(uuid4())
        event_type = event["event_type"]
        sql = (
            "INSERT INTO deferred_task (uid, created_at, retry_at, event_type, event, "
            "attempts) VALUES (?, ?, ?, ?, ?, ?)"
        )

        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, (uid, now, after, event_type, json.dumps(event), 0))
            self.dbconn.commit()
        finally:
            cursor.close()

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

        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, values)
            return self._to_model(cursor.fetchall())
        finally:
            cursor.close()

    def delete(self, uid: str) -> None:
        """
        Delete row from deferred_task table by uid

        Args:
            uid: UID of row to delete

        Returns:
            None
        """
        sql = "DELETE FROM deferred_task WHERE uid=?"
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, (uid,))
            self.dbconn.commit()
        finally:
            cursor.close()

    def _to_model(self, rows: list[list[Any]]) -> list[DeferredTask]:
        """Convert rows into DeferredTask model."""
        return [DeferredTask(*row) for row in rows]
