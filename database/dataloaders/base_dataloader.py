from airflow.utils.log.logging_mixin import LoggingMixin

def get_bridge_key(func):
        def inner(*args, **kwargs):
            db = kwargs['conn_db']
            sql = "SELECT {} FROM {} WHERE {};".format(
                kwargs["select_col"],
                kwargs["bridge_table_name"],
                kwargs["where_clause"]
            )
            df = db.execute_query(sql)
            func(fk_id=df['TickerFinancesID'].values[0], *args, **kwargs)
        return inner

class BaseDataloader(LoggingMixin):
    def __init__(self, db_type):
        self.db = db_type.value

    def _add_str_to_db(self, *args, **kwargs):
        sql = f"""
        INSERT INTO {kwargs['table_name']} ({','.join(kwargs['column_names'])})
        VALUES 
        ({'),\n('.join(','.join(row) for row in args)});
        """
        kwargs['db_context'].execute_query(sql)

    def _dump_df_to_db(self, df, db_context, dest_table_name, full_load=True):
        if full_load:
            db_context.execute_query(f"DELETE FROM {dest_table_name}")
        df.to_sql(
            dest_table_name, 
            con=db_context.engine,
            if_exists='append',
            index=False
        )

    def __call__(self, *args, **kwargs):
        self.main(*args, **kwargs)