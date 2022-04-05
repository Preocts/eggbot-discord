from __future__ import annotations

import datetime
from typing import Any
from uuid import uuid4

from eggbot.model.db_store_intfc import DBStoreIntfc
from eggbot.model.moderation_action import ModerationAction
from eggbot.provider.db_connector import DBConnection


class ModerationActionDB(DBStoreIntfc):

    IntegrityError = DBConnection.IntegrityError

    def __init__(self, db_connection: DBConnection) -> None:
        """CRUD method layer for Moderation Action table"""
        self.dbconn = db_connection

        self._init_table()

    def _init_table(self) -> None:
        """Build table if needed"""
        sql = (
            "CREATE TABLE IF NOT EXISTS moderation_action (uid TEXT PRIMARY KEY, "
            "created_at TEXT, updated_at TEXT, action TEXT, original_note TEXT, "
            "current_note TEXT, active BOOL)"
        )
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql)
            self.dbconn.commit()
        finally:
            cursor.close()

    def row_count(self) -> int:
        """Return total rows in moderation action table"""
        sql = "SELECT COUNT(uid) FROM moderation_action"
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def save(self, event: str, action: str = "note") -> None:
        """
        Save moderation action to database.

        Args:
            event: Reason for moderation action
            action: Type of action take, defaults to 'note' action

        Returns:
            None
        """
        now = datetime.datetime.utcnow()
        sql = (
            "INSERT INTO moderation_action (uid, created_at, updated_at, action, "
            "original_note, current_note, active) VALUES (?, ?, ?, ?, ?, ?, ?)"
        )

        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, (str(uuid4()), now, now, action, event, event, True))
            self.dbconn.commit()
        finally:
            cursor.close()

    def get(self, action: str | None = None) -> list[ModerationAction]:
        """
        Return moderation actions from database

        Args:
            action: Optional filter as to the type of action to return
        """
        if action:
            sql = "SELECT * FROM moderation_action WHERE action=?"
            values = [action]
        else:
            sql = "SELECT * FROM moderation_action"
            values = []

        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, values)
            return self._to_model(cursor.fetchall())
        finally:
            cursor.close()

    def update(self, uid: str, event: str) -> None:
        """
        Save moderation action to database.

        Args:
            uid: UID of record to update
            event: New reason for moderation action

        Returns:
            None
        """
        now = datetime.datetime.utcnow()
        sql = "UPDATE moderation_action SET current_note=?, updated_at=? WHERE uid=?"
        values = (event, now, uid)
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, values)
            self.dbconn.commit()
        finally:
            cursor.close()

    def delete(self, uid: str) -> None:
        """
        Delete row from moderation_action table by uid

        Args:
            uid: UID of row to delete

        Returns:
            None
        """
        sql = "DELETE FROM moderation_action WHERE uid=?"
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql, (uid,))
            self.dbconn.commit()
        finally:
            cursor.close()

    def _to_model(self, rows: list[list[Any]]) -> list[ModerationAction]:
        """Convert rows into DeferredTask model."""
        return [ModerationAction(*row) for row in rows]
