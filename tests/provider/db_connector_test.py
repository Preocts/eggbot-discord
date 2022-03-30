from typing import Generator

import pytest

from eggbot.provider.db_connector import DBConnection
from eggbot.provider.db_connector import DBConnector

DB_URL = "database/"
DB_USER = None
DB_PASSWORD = None
DB_PORT = 1433
DB_FILE = ":memory:"


@pytest.fixture
def provider() -> Generator[DBConnector, None, None]:
    conn = DBConnector(DB_URL, DB_USER, DB_PASSWORD, port=DB_PORT)
    try:
        yield conn
    finally:
        conn.close_all()


def test_init(provider: DBConnector) -> None:
    assert provider.url == DB_URL
    assert provider.user == DB_USER
    assert provider.password == DB_PASSWORD
    assert provider.port == DB_PORT
    assert provider._active == {}


def test_get_connection(provider: DBConnector) -> None:
    with provider.get_connection(DB_FILE) as connection:
        assert DB_FILE in provider._active
        assert isinstance(connection, DBConnection)

    assert provider._active == {}


def test_cached_connection(provider: DBConnector) -> None:
    with provider.get_connection(DB_FILE) as connection01:
        with provider.get_connection(DB_FILE) as connection02:

            assert connection02._dbconn is connection01._dbconn
