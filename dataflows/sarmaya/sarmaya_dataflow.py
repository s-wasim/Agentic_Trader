import time
import re
import os
import json

from dataflows.base_web import BaseWebDriver
from dataflows.sarmaya.sarmaya_helpers import create_table_helper, dump_in_directory

import pandas as pd
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SarmayaDataflow(BaseWebDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = 'https://sarmaaya.pk/'

    def get_page_detail(self, extension_url, data_gate_id, wait_time=2):
        shariah_link = f'{self.base_url}{extension_url}'
        # Get page
        self.driver.get(shariah_link)
        time.sleep(wait_time)
        return [*map(
            lambda x: (x.split('/')[-1], x), 
            [
                re.search(pattern=rf'<a href="{self.base_url}(.*?)"', string=elem[0]).group(1)
                for elem in self.driver.execute_script(f"return $('#{data_gate_id}').DataTable().data().toArray()")
            ]
        )]

    @create_table_helper
    def create_table_normal(self, *args, **kwargs):
        tables = []
        for table in kwargs['soup_obj'].select('table'):
            # Extract headers
            tbl_data = {th.get_text(strip=True): [] for th in table.select('thead tr th')}
            # Extract rows
            for row in table.select('tbody tr'):
                for header, cell in zip(tbl_data.keys(), row.find_all('td')):
                    tbl_data[header].append(cell.get_text(strip=True))
            tables.append(pd.DataFrame(tbl_data))
        return tables 
    @create_table_helper
    def create_table_pivoted(self, *args, **kwargs):
        tables = []
        for table in kwargs['soup_obj'].select('table'):
            # Extract headers
            tbl_data = {}
            for i, row in enumerate(table.select('tbody tr')):
                cells = row.find_all('th') if i == 0 else row.find_all('td')
                header = cells[0].get_text(strip=True)
                values = [cell.get_text(strip=True) for cell in cells[1:]]
                if len(header) == len(values) == 0:
                    continue
                tbl_data[header] = values
            if len(tbl_data['Year']) == 0:
                if len(tables) == 0:
                    return []
                tbl_data['Year'] = tables[-1]['Year'].values.tolist()
            tables.append(pd.DataFrame(tbl_data))
        return tables
    @create_table_helper
    def get_ticker_price_history(self, *args, **kwargs):
        # Use regex to extract jsonfile variable
        match = re.search(r'var jsonfile = (.*);\n', kwargs['response_text'])
        temp = json.loads(match.group(1))
        return [pd.DataFrame.from_dict({
            'year': [data['s_date'] for data in temp['data']], 
            'price': [data['s_close'] for data in temp['data']]
        })]

    def get_ticker_detail(self, extension_url, wait_time=2): 
        EXTRACT_GROUPS = {
            "Payouts": self.create_table_normal,
            "Technicals": self.create_table_normal,
            "Financials": self.create_table_pivoted,
            "20y": self.get_ticker_price_history
        }
        ticker_link = f'{self.base_url}{extension_url}#peers'
        # Get page
        self.driver.get(ticker_link)
        time.sleep(wait_time)
        # Wait until nav-tab div appears (DOM is fully injected now)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'nav-tab'))
        )
        # Scroll to the bottom to trigger DOM population
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        # Find the tab by href
        return {
            a_tag.text if a_tag.text != '20y' else 'Price': EXTRACT_GROUPS[a_tag.text](get_url=a_tag.get_attribute('href'))
            for a_tag in self.driver.find_elements(By.CSS_SELECTOR, '#nav-tab a')
            if a_tag.text in EXTRACT_GROUPS.keys()
        }

    def main(self, *args, **kwargs):
        self.__enter__()
        try:
            # Get all share links
            links = self.get_page_detail(extension_url='psx/market/KMIALLSHR', data_gate_id='stock-screener')
            # Create Store_Files directory if it doesn't exist
            base_dir = os.path.join(os.getcwd(), kwargs['store_dir'])
            os.makedirs(base_dir, exist_ok=True)

            with tqdm(links, desc="Processing tickers", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {postfix}]", postfix=dict(ticker="None")) as pbar:
                for link in pbar:
                    ticker = link[0]
                    pbar.set_postfix(ticker=ticker)
                    # Skip if ticker folder already exists
                    if os.path.exists(os.path.join(base_dir, ticker)):
                        continue
                    # Get data
                    symbol_data = self.get_ticker_detail(extension_url=link[1])
                    # dump in directory
                    dump_in_directory(base_dir, ticker, symbol_data)
                    time.sleep(5) # Nap for 5 seconds to ensure requests don't get blocked
        except Exception as e:
            raise e
        finally:
            self.__exit__()