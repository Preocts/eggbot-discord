from eggbot.provider.db_connector import DBConnection


class DeferredTaskDB:
    def __init__(self, db_connection: DBConnection) -> None:
        """CRUD method layer for Deferred Task table"""
        self.dbconn = db_connection

        self._init_table()

    def _init_table(self) -> None:
        """Build table if needed"""
        sql = (
            "CREATE TABLE IF NOT EXISTS deferred_task"
            "(created_at TEXT, retry_at Text, event TEXT, attempts INT)"
        )
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(sql)
            self.dbconn.commit()
        finally:
            cursor.close()
