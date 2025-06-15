import os
import re
import numpy as np
import pandas as pd

class SarmayaDataprocessor:
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
    
DATA_PROC_FUNCS = {
    'Financials': SarmayaDataprocessor.process_financial_dfs,
    'Payouts': SarmayaDataprocessor.process_payout_dfs,
    'Price': SarmayaDataprocessor.process_price_dfs,
    'Technicals': SarmayaDataprocessor.process_technical_dfs
}

if __name__ == '__main__':
    df = pd.read_csv('Store_Files\SEARL\Price\SEARL_Price_0_20250615_160856.csv')
    base_dir = 'Store_Files\SEARL'
    dfs = []
    for folder in os.listdir(base_dir):
        dfs.append(DATA_PROC_FUNCS[folder]([
            pd.read_csv(os.path.join(base_dir, folder, file)) 
            for file in os.listdir(os.path.join(base_dir, folder))
        ]))
    print(dfs)
    