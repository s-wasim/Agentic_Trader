
from datetime import datetime, date
from airflow.operators.python import get_current_context
from airflow.decorators import task, dag

from dataflows import SarmayaDataflow, KSEStocksDataflow # Extract libs
from dataprocessors import SarmayaDataprocessor # Transform libs
from database import SarmayaDataloader, DBTypes # Load Libs
from helpers import executer, enable_debug_logging

@dag(
    dag_id="PSX_ETL_FLOW_DAG",
    start_date=datetime(2025, 7, 18),
    schedule="@daily",
    catchup=False,
    tags=["ETL", "Web-Scraping"],
    params={"refresh": True, "log_level": "debug", "retries": 10}
)
def psx_etl_flow_dag():
    @task
    def start():
        context = get_current_context()
        print(context["params"]["log_level"])
        if context["params"]["log_level"].lower() == "debug":
            print("DEBUGGER RUNS IDKY")
            enable_debug_logging()
        return context["params"]

    @task
    def extract(parameters):
        executer({
            SarmayaDataflow: {
                'init_args': ['firefox'],
                'use_context': True, 
                'kwargs': {'store_dir': 'Store_Files', 'retries': parameters['retries'], 'nap_time': 1, 'refresh': parameters['refresh']}
            },
            KSEStocksDataflow: {'init_args': [], 'use_context': False, 'kwargs': {'store_dir': "Save_Files"}}
        })

    @task
    def transform():
        executer({
            SarmayaDataprocessor(): {'read_dir': 'Store_Files', 'store_dir': 'Save_Files'}
        })

    @task
    def load():
        executer({
            SarmayaDataloader(DBTypes.MYSQL_DB): {'base_path': 'Save_Files', 'host': 'mysql'}
        })
    parameters = start()
    e, t, l = extract(parameters), transform(), load()
    e >> t >> l

dag = psx_etl_flow_dag()