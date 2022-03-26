import random
from typing import Any
from typing import Generator

import pytest

from eggbot.model.chat_message import ChatMessage
from eggbot.module.keyword_notifi import KeywordNotifi
from eggbot.module.keyword_notifi import KeywordNotifiConfig

random.seed()


def mock_configs(size: int) -> dict[str, Any]:
    """Mocks the return of a loaded config from the unwritten loader"""
    config: dict[str, Any] = {"keyword_notifi": []}
    for idx in range(size):
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


@pytest.mark.parametrize(
    ("message", "expected"),
    (
        ("this is a test", False),
        ("this is another test", False),
        ("this has the keyword", True),
    ),
)
def test_process_message(module: KeywordNotifi, message: str, expected: bool) -> None:
    chat = ChatMessage("123", "0", message)
    result = module.process_message(chat)

    assert result is expected


@pytest.mark.parametrize(
    ("size"),
    (1, 10, 100, 10_000),
)
def test_load_config(size: int, module: KeywordNotifi) -> None:
    config = mock_configs(size)

    module.load_config(config)

    assert len(module.config) == size
