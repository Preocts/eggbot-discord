import sqlite3
from typing import Generator

import pytest

from eggbot.provider.db_connector import DBConnection
from eggbot.provider.moderation_action_db import ModerationActionDB

DB_FILE = ":memory:"
EXPECTED_COLUMNS = [
    "uid",
    "created_at",
    "updated_at",
    "member_id",
    "action",
    "original_note",
    "current_note",
    "active",
]
TABLE_NAME = "moderation_action"
EVENT = "This is moderation event note"


@pytest.fixture
def provider() -> Generator[ModerationActionDB, None, None]:
    dbconn = DBConnection(sqlite3.connect(DB_FILE))
    db_provider = ModerationActionDB(dbconn)
    try:
        yield db_provider
    finally:
        dbconn.close()


def test_init(provider: ModerationActionDB) -> None:
    assert isinstance(provider.dbconn, DBConnection)


def test_row_count(provider: ModerationActionDB) -> None:
    result = provider.row_count()

    assert result == 0


def test_table_create(provider: ModerationActionDB) -> None:
    cursor = provider.dbconn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    col_names = [desc[0] for desc in cursor.description]

    result = set(col_names) - set(EXPECTED_COLUMNS)

    assert len(result) == 0


@pytest.mark.parametrize(("row_count"), (1, 10, 100, 10_000))
def test_save(provider: ModerationActionDB, row_count: int) -> None:
    for _ in range(row_count):
        provider.save(EVENT, action="note")

    assert provider.row_count() == row_count


def test_get_all(provider: ModerationActionDB) -> None:
    total = 10
    for _ in range(total):
        provider.save(EVENT)

    results = provider.get()

    assert len(results) == total


def test_get_by_event_type(provider: ModerationActionDB) -> None:
    total = 10
    for _ in range(total):
        provider.save(EVENT, action="warn")
        provider.save(EVENT, action="ban")

    result01 = provider.get("warn")
    result02 = provider.get("ban")

    assert len(result01) == total
    assert len(result02) == total


def test_delete(provider: ModerationActionDB) -> None:
    provider.save(EVENT)
    row = provider.get()[0]

    provider.delete(row.uid)
    validate = provider.row_count()

    assert validate == 0


def test_update_event(provider: ModerationActionDB) -> None:
    provider.save(EVENT)
    row = provider.get()[0]

    provider.update(row.uid, "This is a new message")
    verify = provider.get()[0]

    assert verify.original_note == row.current_note
    assert verify.current_note == "This is a new message"
    assert verify.created_at == row.created_at
    assert verify.updated_at != row.updated_at


def test_deactivate_action(provider: ModerationActionDB) -> None:
    provider.save(EVENT)
    row = provider.get()[0]

    provider.deactivate(row.uid)
    verify = provider.get()[0]

    assert row.active is True
    assert verify.active is False


def test_get_by_id_active(provider: ModerationActionDB) -> None:
    count = 10
    for _ in range(count):
        provider.save(EVENT)
    uid = provider.get()[-1].uid
    provider.deactivate(uid)

    all_results = provider.get_by_id("egg")
    active_results = provider.get_by_id("egg", True)
    inactive_results = provider.get_by_id("egg", False)

    assert len(all_results) == count
    assert len(active_results) == count - 1
    assert len(inactive_results) == 1
