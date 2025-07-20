import os
import re
import numpy as np
import pandas as pd
from tqdm import tqdm
from shutil import rmtree
from dataprocessors.base_processor import BaseProcessor
from database.connectors import MysqlConnector

class SarmayaDataprocessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.__DATA_PROC_FUNCS = {
            'Financials': SarmayaDataprocessor.process_financial_dfs,
            'Payouts': SarmayaDataprocessor.process_payout_dfs,
            'Price': SarmayaDataprocessor.process_price_dfs,
            'Technicals': SarmayaDataprocessor.process_technical_dfs
        }

    @property
    def data_processing_functions(self):
        return self.__DATA_PROC_FUNCS

    @staticmethod
    def process_financial_dfs(dataframes):
        def proc_col(column):
            # Class-level constants
            POSTFIX_TRANSFORM = {'M': 1000000, 'B': 1000000000}
            PATTERN = re.compile(r'([-\d.]+)\s*([A-Za-z]+)?')
            # Early return for dash
            if column == '-':
                return 0.0
            match = PATTERN.match(str(column))
            numeric, postfix = match.groups()
            try:
                return float(numeric) * POSTFIX_TRANSFORM.get(postfix.upper(), 1) if postfix else float(numeric)
            except ValueError:
                return 0.0
        for dataframe in dataframes:
            for col in dataframe:
                if col == 'Year':
                    dataframe[col] = dataframe[col].apply(int)
                else:
                    dataframe[col] = dataframe[col].apply(proc_col)
        return dataframes
    
    @staticmethod
    def process_payout_dfs(dataframes):
        for dataframe in dataframes:
            dataframe['Year'] = pd.to_datetime(dataframe['Year'], format='%Y-%m-%d')
            dataframe['Face Value'] = pd.to_numeric(dataframe['Face Value'])
        return dataframes
    
    @staticmethod
    def process_price_dfs(dataframes):
        for dataframe in dataframes:
            dataframe['year'] = pd.to_datetime(
                dataframe['year'].apply(lambda x: x.strip('"')), format='%b %d, %y'
            )
            dataframe['price'] = pd.to_numeric(dataframe['price'])
            dataframe.columns = ['Year', 'Price']
        return dataframes
    
    @staticmethod
    def process_technical_dfs(dataframes):
        def proc_value(column):
            return [*map(float, column.strip('"').split(','))]
        df1 = dataframes[0]
        df1['Indicator'] = df1['Indicator'].apply(lambda x: x.strip('"').upper())
        df1['Value'] = df1['Value'].apply(proc_value)
        if len(dataframes) > 1:
            df2 = dataframes[1]
            df2['Action'] = np.nan
            return pd.concat([df1, df2], axis=0)
        return df1
    
    def main(self, *args, **kwargs):
        read_dir, store_dir = list(map(lambda x: os.path.join(os.getcwd(), x), [kwargs['read_dir'], kwargs['store_dir']]))
        tickers = os.listdir(read_dir)
        if os.path.exists(store_dir):
            for entry in os.listdir(store_dir):
                _ = os.path.join(store_dir, entry)
                if os.path.isdir(_):
                    rmtree(_)
        else:
            os.mkdir(store_dir)
        with tqdm(
            tickers, desc="Processing tickers", 
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}",
            postfix="ticker: None"
        ) as pbar:
            for ticker in pbar:
                pbar.set_postfix(ticker=ticker)
                ticker_read_path = os.path.join(read_dir, ticker)
                if ticker_read_path.endswith('csv'):
                    continue
                ticker_store_path = os.path.join(store_dir, ticker)
                os.makedirs(ticker_store_path, exist_ok=True)

                for file_type in os.listdir(ticker_read_path):
                    type_read_path = os.path.join(ticker_read_path, file_type)
                    type_store_path = os.path.join(ticker_store_path, file_type)
                    os.makedirs(type_store_path, exist_ok=True)

                    file_paths = [
                        os.path.join(type_read_path, file_name)
                        for file_name in os.listdir(type_read_path)
                    ]
                    dataframes = [pd.read_csv(fp) for fp in file_paths]
                    if len(dataframes) == 0:
                        continue
                    processed_dfs = self.data_processing_functions[file_type](dataframes)

                    for file_name, processed_df in zip(
                        os.listdir(type_read_path), 
                        processed_dfs if isinstance(processed_dfs, list) else [processed_dfs]
                    ):
                        processed_df.to_csv(os.path.join(type_store_path, file_name), index=False)

    