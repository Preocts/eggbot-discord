"""Abstracts details of a chat message from Discord provider."""
import dataclasses


@dataclasses.dataclass(frozen=True)
class ChatMessage:
    """Abstracts details of a chat message from Discord provider."""

    member_id: str
    channel_id: str
    created_at: str
    raw_message: str
