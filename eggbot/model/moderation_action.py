from __future__ import annotations

import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class ModerationAction:
    """Model row for moderation_action table"""

    # NOTE: Order of attributes must match table schema
    uid: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    member_id: str
    action: str
    original_note: str
    current_note: str
    active: bool

    @classmethod
    def from_row(
        cls,
        uid: str,
        created_at: str,
        updated_at: str,
        member_id: str,
        action: str,
        original_note: str,
        current_note: str,
        active: int,
    ) -> ModerationAction:
        """Generate object from table row"""
        # Handles lack of types available in sqllite3
        return ModerationAction(
            uid=uid,
            created_at=datetime.datetime.fromisoformat(created_at),
            updated_at=datetime.datetime.fromisoformat(updated_at),
            member_id=member_id,
            action=action,
            original_note=original_note,
            current_note=current_note,
            active=bool(active),
        )
