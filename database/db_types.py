from enum import Enum
from database.connectors.mysql.mysql_connector import MysqlConnector

class DBTypes(Enum):
    MYSQL_DB=MysqlConnector