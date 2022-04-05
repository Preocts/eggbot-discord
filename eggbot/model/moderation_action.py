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
