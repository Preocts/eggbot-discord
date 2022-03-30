import sqlite3
from typing import Generator

import pytest

from eggbot.provider.db_connector import DBConnection
from eggbot.provider.deferred_task_db import DeferredTaskDB

DB_FILE = ":memory:"
EXPECTED_COLUMNS = ["created_at", "retry_at", "event", "attempts"]
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


def test_table_create(provider: DeferredTaskDB) -> None:
    cursor = provider.dbconn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    col_names = [desc[0] for desc in cursor.description]

    result = set(col_names) - set(EXPECTED_COLUMNS)

    assert len(result) == 0
