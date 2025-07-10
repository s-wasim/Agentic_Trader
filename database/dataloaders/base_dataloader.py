from database.connectors.mysql import MysqlConnector

class BaseDataloader:
    def __init__(self, db_type):
        self.db = db_type.value

    def _dump_df_to_db(self, df, db_context, dest_table_name):
        df.to_sql(
            dest_table_name, 
            con=db_context.engine,
            if_exists='append',
            index=False
        )