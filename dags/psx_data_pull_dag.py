from dataflows import SarmayaDataflow, KSEStocksDataflow # Extract libs
from dataprocessors import SarmayaDataprocessor # Transform libs
from database import SarmayaDataloader, DBTypes # Load Libs
from dags.helper import execute_callable
from airflow.decorators import dag, task
from datetime import datetime

@task
def extract():
    execute_callable({
        SarmayaDataflow: {
            'init_args': ['firefox'],
            'use_context': True, 
            'kwargs': {'store_dir': 'Store_Files', 'retries': 5, 'nap_time': 1}
        },
        KSEStocksDataflow: {'init_args': [], 'use_context': False, 'kwargs': {'store_dir': "Save_Files"}}
    })

@task
def transform():
    execute_callable({
        SarmayaDataprocessor(): {'read_dir': 'Store_Files', 'store_dir': 'Save_Files'}
    })

@task
def load():
    execute_callable({
        SarmayaDataloader(DBTypes.MYSQL_DB): {'base_path': 'Save_Files'}
    })

@dag(start_date=datetime(2023, 1, 1), schedule="@daily", catchup=False)
def psx_data_pull():
    extracted = extract()
    transformed = transform()
    loaded = load()

    # Define the task execution order
    extracted >> transformed >> loaded

dag = psx_data_pull()