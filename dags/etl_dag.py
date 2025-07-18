
from datetime import datetime, date
from airflow.decorators import task, dag

from dataflows import SarmayaDataflow, KSEStocksDataflow # Extract libs
from dataprocessors import SarmayaDataprocessor # Transform libs
from database import SarmayaDataloader, DBTypes # Load Libs
from helpers import executer

@dag(
    dag_id="PSX_ETL_FLOW_DAG",
    start_date=datetime(2025, 7, 18),
    schedule="@daily",
    catchup=False,
    tags=["ETL", "Web-Scraping"]
)
def psx_etl_flow_dag():
    @task
    def extract():
        executer({
            SarmayaDataflow: {
                'init_args': ['firefox'],
                'use_context': True, 
                'kwargs': {'store_dir': 'Store_Files', 'retries': 5, 'nap_time': 1, 'refresh': True}
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
            SarmayaDataloader(DBTypes.MYSQL_DB): {'base_path': 'Save_Files'}
        })
    
    e, t, l = extract(), transform(), load()
    e >> t >> l

dag = psx_etl_flow_dag()