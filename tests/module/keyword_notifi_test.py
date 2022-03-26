import random
from ast import literal_eval
from datetime import datetime
from typing import Any
from typing import Generator

import pytest

from eggbot.model.chat_message import ChatMessage
from eggbot.module.keyword_notifi import KeywordNotifi
from eggbot.module.keyword_notifi import KeywordNotifiConfig

random.seed()

MEMBER_ID = "12345678901234567"
CHANNEL_ID = "01234567890123456"
MATCH_PATTERN = "Jeff(erson|)"


def mock_configs(size: int) -> dict[str, Any]:
    """Mocks the return of a loaded config from the unwritten loader"""
    config: dict[str, Any] = {"keyword_notifi": []}

    config["keyword_notifi"].append(
        {
            "member_id": MEMBER_ID,
            "pattern": MATCH_PATTERN,
            "enabled": True,
            "block_list": [],
        }
    )

    for idx in range(size - len(config)):
        member = {
            "member_id": f"123-{idx}",
            "pattern": "{idx}",
            "enabled": random.choice([True, False]),
            "block_list": [],
        }
        config["keyword_notifi"].append(member)
    return config


@pytest.fixture
def module() -> Generator[KeywordNotifi, None, None]:
    module = KeywordNotifi()
    module.load_config(mock_configs(10))
    yield module


# fmt: off
@pytest.mark.parametrize(
    ("message", "expected"),
    (
        ("you don't have to test all your code, only the parts that you want to work.", False),
        ("bent pipes <>, curly bois {}, staples [], pillows (), from-the-windows, to-the-walls /", False),
        ("Jefferson is a icon of the USD currency", True),
        ("It wasn't like Jeff had any choice", True),
        ("This is a weirdjefferson sentance", False),
        ("Hey <@12345678901234567>, you vibin'?", True),
    ),
)
# fmt: on
def test_process_message(module: KeywordNotifi, message: str, expected: bool) -> None:
    chat_message = ChatMessage(
        member_id=MEMBER_ID,
        channel_id=CHANNEL_ID,
        created_at=str(datetime.utcnow()),
        raw_message=message,
    )

    result = module.process_message(chat_message)

    assert bool(result) is expected


@pytest.mark.parametrize(
    ("size"),
    (1, 10, 100, 10_000),
)
def test_load_config(size: int, module: KeywordNotifi) -> None:
    config = mock_configs(size)

    module.load_config(config)

    assert len(module.configs) == size
