"""Abstracts details of a chat message from Discord provider."""
from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class ChatMessage:
    """Abstracts details of a chat message from Discord provider."""

    member_id: str
    channel_id: str
    created_at: str
    raw_message: str
