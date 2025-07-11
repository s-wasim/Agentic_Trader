import os
import time
from tqdm import tqdm
from dataflows import SarmayaDataflow, sarmay_dump_in_directory
from selenium.common.exceptions import StaleElementReferenceException

with SarmayaDataflow("firefox") as dataflow:
    # Get all share links
    links = dataflow.get_page_detail(extension_url='psx/market/KMIALLSHR', data_gate_id='stock-screener')
    # Create Store_Files directory if it doesn't exist
    base_dir = os.path.join(os.getcwd(), 'Store_Files')
    os.makedirs(base_dir, exist_ok=True)
attempts, max_allowed = 0, 15
while attempts < max_allowed:
    try:
        with SarmayaDataflow("firefox") as dataflow:
            with tqdm(links, desc="Processing tickers", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {postfix}]", postfix=dict(ticker="None")) as pbar:
                for link in pbar:
                    ticker = link[0]
                    pbar.set_postfix(ticker=ticker)
                    # Skip if ticker folder already exists
                    if os.path.exists(os.path.join(base_dir, ticker)):
                        continue
                    # Get data
                    symbol_data = dataflow.get_ticker_detail(extension_url=link[1], wait_time=10)
                    # dump in directory
                    sarmay_dump_in_directory(base_dir, ticker, symbol_data)
    except StaleElementReferenceException as e:
        print("ERR: DOM NOT FULLY INJECTED\nQuitting driver and restarting process")
        attempts += 1
        time.sleep(10)
    attempts = max_allowed + 1
print(f"Total attempts needed: {attempts}/{max_allowed}")