import os
from datetime import datetime

from bs4 import BeautifulSoup
import requests

def create_table_helper(func):
    def create_table(*args, **kwargs):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(kwargs['get_url'], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return func(soup_obj=soup, response_text=response.text, *args, **kwargs)
    return create_table

def dump_in_directory(base_dir, ticker, symbol_data):
    # Create ticker directory
    ticker_dir = os.path.join(base_dir, ticker)
    os.makedirs(ticker_dir, exist_ok=True)
    # Current timestamp for file naming
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Process each category (Payouts, Technicals, Financials)
    for category, dataframes in symbol_data.items():
        # Create category subdirectory
        category_dir = os.path.join(ticker_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        # Save each dataframe in the list
        for i, df in enumerate(dataframes):
            filename = f"{ticker}_{category}_{i}_{timestamp}.csv"
            df.to_csv(os.path.join(category_dir, filename), index=False)