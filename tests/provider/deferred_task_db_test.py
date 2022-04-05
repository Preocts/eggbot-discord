import json
import sqlite3
from typing import Generator

import pytest

from eggbot.provider.db_connector import DBConnection
from eggbot.provider.deferred_task_db import DeferredTaskDB

DB_FILE = ":memory:"
EXPECTED_COLUMNS = ["uid", "created_at", "retry_at", "event_type", "event", "attempts"]
TABLE_NAME = "deferred_task"
TASK = '{"event_type": "remind", "message": "get eggs"}'


@pytest.fixture
def provider() -> Generator[DeferredTaskDB, None, None]:
    dbconn = DBConnection(sqlite3.connect(DB_FILE))
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

    for _ in range(row_count):
        provider.save(TASK, "testing", 100)

    assert provider.row_count() == row_count


def test_get_all(provider: DeferredTaskDB) -> None:
    total = 10
    for _ in range(total):
        provider.save(TASK)

    results = provider.get()

    assert len(results) == total


def test_get_by_event_type(provider: DeferredTaskDB) -> None:
    total = 10
    for _ in range(total):
        provider.save(TASK, "remind")
        provider.save(TASK, "announce")

    result01 = provider.get("remind")
    result02 = provider.get("announce")

    assert len(result01) == total
    assert len(result02) == total


def test_delete(provider: DeferredTaskDB) -> None:
    provider.save(TASK)
    row = provider.get()[0]

    provider.delete(row.uid)
    validate = provider.row_count()

    assert validate == 0
