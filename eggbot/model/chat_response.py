"""Model used to pass response actions back from a chat module"""
from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ChatResponse:
    """Model used to pass response actions back from a chat module"""

    message: str
    target_id: str
    delivery_id: str | None
