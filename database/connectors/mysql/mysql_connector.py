import pandas as pd
from sqlalchemy import create_engine
from database.connectors import BaseConnector
from helpers.env_vars import ENV_VARS

class MysqlConnector(BaseConnector):
    def __init__(self, host, user, database):
        super().__init__(host, user, database)
        self._create_connection(password=ENV_VARS.MYSQL_CONNECTOR_PASSWORD.value)
        self._engine = create_engine('mysql+mysqlconnector://', creator=lambda: self._connection)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'connection') and self._connection:
            self._connection.close()

    def execute_query(self, query, *args, **kwargs):
        res_set = super().execute_query(query, *args, **kwargs)
        return pd.DataFrame(
            res_set,
            columns=[col[0] for col in self._cursor.description]
        ) if len(res_set) > 0 else None

    @property
    def engine(self):
        return self._engine

if __name__ == "__main__":
    with MysqlConnector('localhost', 'root', 'AGENTIC_TRADER') as db:
        res = db.execute_query("SELECT * FROM TEST;")
        print(res)