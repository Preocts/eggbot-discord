import dataclasses
import datetime
from typing import Any


@dataclasses.dataclass
class DeferredTask:
    """Model mirrors DeferredTask row from deferred_task table"""

    # NOTE: Order of attributes must match table schema
    uid: str
    created_at: datetime.datetime
    retry_at: datetime.datetime
    event_type: str
    event: dict[str, Any]
    attempts: int
