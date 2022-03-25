from typing import Generator

import pytest

from eggbot.model.chat_message import ChatMessage
from eggbot.module.keyword_notifi import KeywordNotifi


@pytest.fixture
def module() -> Generator[KeywordNotifi, None, None]:
    yield KeywordNotifi()


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
