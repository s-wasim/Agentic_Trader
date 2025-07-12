import os

import pandas as pd
from tqdm import tqdm

from database.db_types import DBTypes
from database.dataloaders.base_dataloader import BaseDataloader, get_bridge_key

class SarmayaDataloader(BaseDataloader):
    def __init__(self, destination_database):
        self.tbl_mapping = {
            'Price':{
                'tbl_name': 'PriceHistory',
                'columns': ['PriceDate', 'Price']
            },
            'Technicals':{
                'tbl_name': 'TechnicalIndicators',
                'columns': ['IndicatorName', 'IndicatorValue', 'IndicatorAction']
            },
            'Payouts':{
                'tbl_name': 'Payouts',
                'columns': ['PayoutDate', 'PayoutType', 'FaceValue', 'PayoutPercent']
            }
        }
        super().__init__(destination_database)
    
    @get_bridge_key
    def __load_financials(self, fk_id, *args, **kwargs):
        df = pd.read_csv(kwargs['file_name'])
        df = pd.melt(
            df, id_vars=['Year'],
            value_vars=set(df.columns.tolist()).remove('Year'),
            var_name='MetricName', value_name='MetricValue'
        )
        df['TickerFinancesID'] = fk_id
        self._dump_df_to_db(df, kwargs['conn_db'], kwargs['table_name'], False)        

    def main(self, *args, **kwargs):
        base_path = os.path.join(os.getcwd(), kwargs['base_path'])
        with self.db('localhost', 'root', 'AGENTIC_TRADER') as db,\
            tqdm(
                os.listdir(base_path), desc="Processing tickers", 
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {postfix}]", 
                postfix=dict(ticker="None")
            ) as pbar:
            file_path = os.path.join(base_path, 'ticker_details.csv')
            df = pd.read_csv(file_path)
            self._dump_df_to_db(df, db, 'Ticker')
            for ticker_name in pbar:
                pbar.set_postfix(ticker=ticker_name)
                if ticker_name.endswith('csv'):
                    continue
                if db.execute_query(f"SELECT * FROM Ticker WHERE TickerName='{ticker_name}'") is None:
                    continue
                for file_type in os.listdir(os.path.join(base_path, ticker_name)):
                    match file_type:
                        case 'Financials':
                            for file, finances_type in zip(
                                os.listdir(os.path.join(base_path, ticker_name, file_type)),
                                ['IncomeStatement','BalanceSheet','CashFlow','Ratios','Dividends']
                            ):
                                self._add_str_to_db(
                                    [f"'{ticker_name}'", f"'{finances_type}'"],
                                    table_name='Ticker_Financials',
                                    column_names=['TickerName', 'FinancialsType'],
                                    db_context=db
                                )
                                self.__load_financials(
                                    conn_db = db, 
                                    select_col = 'TickerFinancesID',
                                    bridge_table_name = 'Ticker_Financials',
                                    table_name = 'Financial_Details',
                                    where_clause = f"TickerName='{ticker_name}' AND FinancialsType='{finances_type}'",
                                    file_name = os.path.join(base_path, ticker_name, file_type, file)
                                )
                        case _:
                            files = os.listdir(os.path.join(base_path, ticker_name, file_type))
                            if len(files) == 0:
                                continue
                            file = files[0]
                            df = pd.read_csv(os.path.join(base_path, ticker_name, file_type, file))
                            df.columns = self.tbl_mapping[file_type]['columns']
                            df['TickerName'] = ticker_name
                            self._dump_df_to_db(df, db, self.tbl_mapping[file_type]['tbl_name'], False)
