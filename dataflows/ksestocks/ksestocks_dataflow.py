import os
from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

class KSEStocksDataflow:
    def __init__(self):
        self.base_url = 'https://www.ksestocks.com/ListedCompanies'
        response = requests.get(self.base_url)
        self.soup = bs(response.content, 'html.parser')

    def get_table(self):
        table = self.soup.find(name='table')
        df = pd.read_html(StringIO(str(table)), flavor='lxml')[0].iloc[1:,[0,1]]
        modified_data = {
            'TickerName':[], 'CompanyName':[], 'Sector':[], 'IsActive':[]
        }
        sector = None

        for _, row in df.iterrows():
            if row[0] == "Symbol":
                sector = row[0]  # Technically redundant, but keeps logic consistent
                continue
            if sector:
                modified_data['TickerName'].append(row[0])
                modified_data['CompanyName'].append(row[1])
                modified_data['Sector'].append(sector)
                modified_data['IsActive'].append(True)
        return pd.DataFrame(modified_data)

if __name__ == "__main__":
    dataflow = KSEStocksDataflow()
    base_dir = os.path.join(os.getcwd(), 'Store_Files')
    df = dataflow.get_table()
    df.to_csv(os.path.join(base_dir, 'ticker_details.csv'), index=False)