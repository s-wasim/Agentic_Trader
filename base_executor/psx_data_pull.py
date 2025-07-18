from dataflows import SarmayaDataflow, KSEStocksDataflow # Extract libs
from dataprocessors import SarmayaDataprocessor # Transform libs
from database import SarmayaDataloader, DBTypes # Load Libs
from helpers import executer

def etl_psx_data():
    # extract
    executer({
        SarmayaDataflow: {
            'init_args': ['firefox'],
            'use_context': True, 
            'kwargs': {'store_dir': 'Store_Files', 'retries': 5, 'nap_time': 1, 'refresh': True}
        },
        KSEStocksDataflow: {'init_args': [], 'use_context': False, 'kwargs': {'store_dir': "Save_Files"}}
    })
    # transform
    executer({
        SarmayaDataprocessor(): {'read_dir': 'Store_Files', 'store_dir': 'Save_Files'}
    })
    # load
    executer({
        SarmayaDataloader(DBTypes.MYSQL_DB): {'base_path': 'Save_Files'}
    })

if __name__ == "__main__":
    etl_psx_data()