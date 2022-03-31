import sqlite3
from typing import Generator

import pytest

from eggbot.provider.db_connector import DBConnection
from eggbot.provider.deferred_task_db import DeferredTaskDB

DB_FILE = ":memory:"
EXPECTED_COLUMNS = ["uid", "created_at", "retry_at", "event_type", "event", "attempts"]
TABLE_NAME = "deferred_task"


@pytest.fixture
def provider() -> Generator[DeferredTaskDB, None, None]:
    dbconn = DBConnection(sqlite3.connect(":memory:"))
    db_provider = DeferredTaskDB(dbconn)
    try:
        yield db_provider
    finally:
        dbconn.close()


def test_init(provider: DeferredTaskDB) -> None:
    assert isinstance(provider.dbconn, DBConnection)


def test_row_count(provider: DeferredTaskDB) -> None:
    result = provider.row_count()

    assert result == 0


def test_table_create(provider: DeferredTaskDB) -> None:
    cursor = provider.dbconn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    col_names = [desc[0] for desc in cursor.description]

    result = set(col_names) - set(EXPECTED_COLUMNS)

    assert len(result) == 0


@pytest.mark.parametrize(("row_count"), (1, 10, 100, 10_000))
def test_save(provider: DeferredTaskDB, row_count: int) -> None:
    task = {"event_type": "remind", "message": "get eggs"}

    for _ in range(row_count):
        provider.save(task, 100)

    assert provider.row_count() == row_count


def test_save_with_uid_error(provider: DeferredTaskDB) -> None:
    task = {"event_type": "remind", "message": "get eggs", "uid": "0"}
    provider.save(task)

    with pytest.raises(provider.IntegrityError):
        provider.save(task)


def test_get_all(provider: DeferredTaskDB) -> None:
    total = 10
    task = {"event_type": "remind", "message": "get eggs"}
    for _ in range(total):
        provider.save(task)

    results = provider.get()

    assert len(results) == total


def test_get_by_event_type(provider: DeferredTaskDB) -> None:
    total = 10
    task01 = {"event_type": "remind", "message": "get eggs"}
    task02 = {"event_type": "announce", "message": "get eggs"}
    for _ in range(total):
        provider.save(task01)
        provider.save(task02)

    result01 = provider.get("remind")
    result02 = provider.get("announce")

    assert len(result01) == total
    assert len(result02) == total


def test_delete(provider: DeferredTaskDB) -> None:
    uid = "test"
    task = {"event_type": "remind", "message": "get eggs", "uid": uid}
    provider.save(task)
    prevalidate = provider.row_count()

    provider.delete(uid)
    validate = provider.row_count()

    assert prevalidate == 1
    assert validate == 0
