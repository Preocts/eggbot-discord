from __future__ import annotations

import datetime
from typing import Any
from uuid import uuid4

from eggbot.model.db_store_intfc import DBStoreIntfc
from eggbot.model.moderation_action import ModerationAction
from eggbot.provider.db_connector import DBConnection


class ModerationActionDB(DBStoreIntfc):
    def __init__(self, db_connection: DBConnection) -> None:
        """CRUD method layer for Moderation Action table"""
        self.dbconn = db_connection

        self._init_table()

    def _init_table(self) -> None:
        """Build table if needed"""
        sql = (
            "CREATE TABLE IF NOT EXISTS moderation_action (uid TEXT PRIMARY KEY, "
            "created_at TEXT, updated_at TEXT, member_id TEXT, action TEXT, "
            "original_note TEXT, current_note TEXT, active BOOL)"
        )
        with self.get_cursor() as cursor:
            cursor.execute(sql)
            self.dbconn.commit()

    def row_count(self) -> int:
        """Return total rows in moderation action table"""
        sql = "SELECT COUNT(uid) FROM moderation_action"
        with self.get_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]

    def save(self, event: str, *, member_id: str = "egg", action: str = "note") -> None:
        """
        Save moderation action to database.

        Args:
            event: Reason for moderation action
            member_id: ID of member actions noted on. Default to 'egg', a catch-all id
            action: Type of action take, defaults to 'note' action

        Returns:
            None
        """
        now = datetime.datetime.utcnow()
        sql = (
            "INSERT INTO moderation_action (uid, created_at, updated_at, member_id, "
            "action, original_note, current_note, active) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )

        with self.get_cursor() as cursor:
            cursor.execute(
                sql,
                (
                    str(uuid4()),
                    now,
                    now,
                    member_id,
                    action,
                    event,
                    event,
                    True,
                ),
            )
            self.dbconn.commit()

    def get(self, action: str | None = None) -> list[ModerationAction]:
        """
        Return moderation actions from database

        Args:
            action: Optional filter as to the type of action to return

        Returns:
            List of ModerationAction objects discovered, can be empty
        """
        if action:
            sql = "SELECT * FROM moderation_action WHERE action=?"
            values = [action]
        else:
            sql = "SELECT * FROM moderation_action"
            values = []

        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            return self._to_model(cursor.fetchall())

    def get_by_id(
        self,
        member_id: str,
        active: bool | None = None,
    ) -> list[ModerationAction]:
        """
        Return moderation action by member id from database

        Args:
            member_id: Member ID to return
            active: If true or false, filter by (in)active actions else all actions

        Returns:
            List of ModerationAction objects discovered, can be empty
        """
        if active is not None:
            sql = "SELECT * FROM moderation_action WHERE active=? and member_id=?"
            values = [active, member_id]
        else:
            sql = "SELECT * FROM moderation_action WHERE member_id=?"
            values = [member_id]

        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            return self._to_model(cursor.fetchall())

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
        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            self.dbconn.commit()

    def delete(self, uid: str) -> None:
        """
        Delete row from moderation_action table by uid

        Args:
            uid: UID of row to delete

        Returns:
            None
        """
        sql = "DELETE FROM moderation_action WHERE uid=?"
        with self.get_cursor() as cursor:
            cursor.execute(sql, (uid,))
            self.dbconn.commit()

    def deactivate(self, uid: str) -> None:
        """
        Mark given record as deactivated

        Args:
            uid: UID of row to deactivate

        Returns:
            None
        """
        sql = "UPDATE moderation_action SET active=? WHERE uid=?"
        values = (False, uid)
        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            self.dbconn.commit()

    def _to_model(self, rows: list[list[Any]]) -> list[ModerationAction]:
        """Convert rows into DeferredTask model."""
        return [ModerationAction.from_row(*row) for row in rows]
