from dataflows import SarmayaDataflow, KSEStocksDataflow # Extract libs
from dataprocessors import SarmayaDataprocessor # Transform libs
from database import SarmayaDataloader, DBTypes # Load Libs

def etl(extract, transform, load):
    if isinstance(extract, dict):
        for e, params in extract.items():
            if params['use_context']:
                with e(*params['init_args']) as extractor:
                    extractor(**params['kwargs'])
            else:
                e(*params['init_args'])(**params['kwargs'])
    else:
        extract()
    if isinstance(transform, dict):
        for t, kwargs in transform.items():
            t(**kwargs)
    else:
        transform()
    if isinstance(load, dict):
        for l, kwargs in load.items():
            l(**kwargs)
    else:
        load()

if __name__ == "__main__":
    etl(
        extract={
            SarmayaDataflow: {
                'init_args': ['firefox'],
                'use_context': True, 
                'kwargs': {'store_dir': 'Store_Files', 'retries': 5, 'nap_time': 1}
            },
            KSEStocksDataflow: {'init_args': [], 'use_context': False, 'kwargs': {'store_dir': "Store_Files"}}
        },
        transform={
            SarmayaDataprocessor(): {'read_dir': 'Store_Files', 'store_dir': 'Save_Files'}
        },
        load={SarmayaDataloader(DBTypes.MYSQL_DB): {'base_path': 'Save_Files'}}
    )
