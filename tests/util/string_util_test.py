from __future__ import annotations

import pytest

from eggbot.util.string_util import StringUtil


@pytest.mark.parametrize(
    ("text", "pattern", "expected"),
    (
        ("This is a test", "^this", True),
        ("Test is a this", "^this", False),
        ("Test is a that", "^this", False),
        ("", "^this", False),
    ),
)
def test_has_match(text: str, pattern: str, expected: str) -> None:
    result = StringUtil.has_match(text, pattern)

    assert result is expected
