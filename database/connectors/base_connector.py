from mysql import connector

class BaseConnector:
    def __init__(self, host, user, database, autocommit=True):
        self._conn_params = {
            'host': host, 
            'user': user,
            'password': None, 
            'database': database,
            'autocommit': autocommit
        }
        self._connection, self._cursor = None, None

    def _create_connection(self, **kwargs):
        self._conn_params.update(kwargs)
        self._connection = connector.connect(**self._conn_params)
        self._cursor = self._connection.cursor()

    @property
    def connection(self):
        return self._connection
    @property
    def cursor(self):
        return self._cursor
    
    def commit(self):
        self.connection.commit()
    
    def execute_query(self, query, *args, **kwargs):
        self._cursor.execute(query, params= args if args else None, **kwargs)
        return self._cursor.fetchall()