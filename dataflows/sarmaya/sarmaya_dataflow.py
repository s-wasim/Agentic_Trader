import time
import re
import os
import json
from shutil import rmtree

from dataflows.base_web import BaseWebDriver
from dataflows.sarmaya.sarmaya_helpers import create_table_helper, dump_in_directory

import pandas as pd
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class SarmayaDataflow(BaseWebDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = 'https://sarmaaya.pk/'
        self.EXTRACT_GROUPS = {
            "Payouts": self.create_table_normal,
            "Technicals": self.create_table_normal,
            "Financials": self.create_table_pivoted,
            "20y": self.get_ticker_price_history
        }
        self.log.info("Initialized SarmayaDataflow")
        self.log.debug("self.base_url")
        self.tries = 3

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
        ticker_link = f'{self.base_url}{extension_url}#peers'
        # Get page
        self.driver.get(ticker_link)
        # Scroll to the bottom to trigger DOM population
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait until nav-tab div appears (DOM is fully injected now)
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#nav-tab a'))
        )
        # Run JS to extract all anchor tag text/hrefs in one shot (safe and fast)
        tags_raw = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('#nav-tab a'))
                .map(a => [a.innerText, a.href]);
        """)
        tags = [(text, href) for text, href in tags_raw if text in self.EXTRACT_GROUPS.keys()]
        # Find the tab by href
        return {
            tag_text if tag_text != '20y' else 'Price': self.EXTRACT_GROUPS[tag_text](get_url=tag_url)
            for tag_text, tag_url in tags
        }

    def main(self, *args, **kwargs):
        # Get all share links
        links = self.get_page_detail(extension_url='psx/market/KMIALLSHR', data_gate_id='stock-screener')
        # Create Store_Files directory if it doesn't exist
        base_dir = os.path.join(os.getcwd(), kwargs['store_dir'])
        if kwargs.get('refresh'):
            self.log.info("Refreshing directories")
            if os.path.exists(base_dir):
                self.log.warning(f"Clearing out base directory {base_dir} in 5 seconds...")
                time.sleep(5)
                rmtree(base_dir)
        os.makedirs(base_dir, exist_ok=True)
        self.log.info("Starting ticker data extract")
        x = 0
        while True:
            try:
                for link in links:
                    ticker = link[0]
                    self.log.info(f"Processing ticker {ticker}")
                    # Skip if ticker folder already exists
                    if os.path.exists(os.path.join(base_dir, ticker)):
                        self.log.info(f"Skipping ticker as it already exists")
                        continue
                    # Get data
                    self.log.debug(f"Getting data from {link[1]}")
                    symbol_data = self.get_ticker_detail(extension_url=link[1])
                    # dump in directory
                    self.log.info("Ticker dumped in directory")
                    dump_in_directory(base_dir, ticker, symbol_data)
                    self.log.info("Ticker fetched")
                    time.sleep(kwargs.get('nap_time', 1)) # Nap for specified time
                break
            except Exception as e:
                self.log.error(f"Error raised when fetching ticker data\n{e}")
                self.log.info(f"Retrying {x}/{self.tries}")
                x += 1
                if x == self.tries:
                    break