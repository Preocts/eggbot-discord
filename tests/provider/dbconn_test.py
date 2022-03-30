from sqlite3 import Connection

from eggbot.provider.dbconn import DBConn

DB_URL = "database/"
DB_USER = None
DB_PASSWORD = None
DB_PORT = 1433
DB_FILE = ":memory:"


def test_init() -> None:
    provider = DBConn(DB_URL, DB_USER, DB_PASSWORD, port=DB_PORT)

    assert provider.url == DB_URL
    assert provider.user == DB_USER
    assert provider.password == DB_PASSWORD
    assert provider.port == DB_PORT
    assert provider._active == {}


def test_get_connection() -> None:
    provider = DBConn()

    with provider.get_connection(DB_FILE):
        assert DB_FILE in provider._active
        assert isinstance(provider._active[DB_FILE], Connection)

    assert provider._active == {}
