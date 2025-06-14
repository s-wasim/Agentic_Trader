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
        return func(soup_obj=soup, *args, **kwargs)
    return create_table