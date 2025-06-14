import time
import re

from helpers.env_vars import ENV_VARS
from dataflows.helper.web_drivers import WEB_DRIVERS
from dataflows.base_web import BaseWebDriver

import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SarmayaDataflow(BaseWebDriver):
    EXTRACT_GROUPS = [
        "Payouts",
        "Technicals",
        "Financials",
    ]
    def __init__(self):
        super().__init__(
            WEB_DRIVERS.CHROME_DRIVER(
                driver_path=ENV_VARS.CHROME_WEB_DRIVER_PATH.value
                )
            )
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
    
    def get_ticker_detail(self, extension_url, wait_time=2):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": None,
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }
        def get_ticker_data(url):
            nonlocal headers
            headers['Referer'] = url
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text

        ticker_link = f'{self.base_url}{extension_url}#peers'
        # Get page
        self.driver.get(ticker_link)
        time.sleep(wait_time)
        # Wait until nav-tab div appears (DOM is fully injected now)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'nav-tab'))
        )
        # Find the tab by href
        return {
            a_tag.text: get_ticker_data(a_tag.get_attribute('href'))
            for a_tag in self.driver.find_elements(By.CSS_SELECTOR, '#nav-tab a')
            if a_tag.text in self.EXTRACT_GROUPS
        }

if __name__ == "__main__":
    with SarmayaDataflow() as dataflow:
        # Get all share links
        # links = dataflow.get_page_detail(extension_url='psx/market/KMIALLSHR', data_gate_id='stock-screener')
        links = [('DCR', 'psx/company/DCR')]
        symbol_data = {}
        for link in links:
            print(f'Getting details for ticker: {link[0]}')
            symbol_data[link[0]] = dataflow.get_ticker_detail(extension_url=link[1])
    print(symbol_data)