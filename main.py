from dataflows import SarmayaDataflow, KSEStocksDataflow # Extract libs
from dataprocessors import SarmayaDataprocessor # Transform libs
from database import SarmayaDataloader, DBTypes # Load Libs

def etl(extract, transform, load):
    if isinstance(extract, dict):
        for e, kwargs in extract.items():
            e(**kwargs)
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
            SarmayaDataflow("firefox"): {'store_dir': 'Store_Files'},
            KSEStocksDataflow(): {'store_dir': "Store_Files"}
        },
        transform={
            SarmayaDataprocessor(): {'read_dir': 'Store_Files', 'store_dir': 'Save_Files'}
        },
        load={SarmayaDataloader(DBTypes.MYSQL_DB): {'base_path': 'Save_Files'}}
    )
