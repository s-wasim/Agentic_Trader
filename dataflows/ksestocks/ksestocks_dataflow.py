import os
from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

class KSEStocksDataflow:
    def __init__(self, *args):
        self.base_url = 'https://www.ksestocks.com/ListedCompanies'
        response = requests.get(self.base_url)
        self.soup = bs(response.content, 'html.parser')

    def get_table(self):
        table = self.soup.find(name='table')
        df = pd.read_html(StringIO(str(table)), flavor='lxml')[0].iloc[1:,[0,1]]
        modified_data = {
            'TickerName':[], 'CompanyName':[], 'Sector':[], 'IsActive':[]
        }
        def update_dict():
            nonlocal modified_data, prev_row, sector
            modified_data['TickerName'].append(prev_row[0])
            modified_data['CompanyName'].append(prev_row[1])
            modified_data['Sector'].append(sector)
            modified_data['IsActive'].append(True)
        prev_row, sector = None, None
        for _, row in df.iterrows():
            if prev_row is None:
                prev_row = row
                continue
            if row[0] == "Symbol": # Found sector, continue.
                sector = prev_row[0]
                prev_row = None
                continue
            update_dict()
            prev_row = row
        update_dict()
        return pd.DataFrame(modified_data)

    def __call__(self, *args, **kwargs):
        base_dir = os.path.join(os.getcwd(), kwargs['store_dir'])
        df = self.get_table()
        df.to_csv(os.path.join(base_dir, 'ticker_details.csv'), index=False)