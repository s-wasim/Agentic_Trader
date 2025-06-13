import functools
from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def initialize_driver(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu")  
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")  
        # Optional: Allow passing extra options dynamically
        for opt in args:
            options.add_argument(opt)
        return func(options, *args, **kwargs)
    return inner


@initialize_driver
def chrome_driver(options=None, *args, **kwargs):
    driver_path = kwargs.get('driver_path')
    if not driver_path:
        raise ValueError("driver_path is required")
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)


class WEB_DRIVERS(Enum):
    CHROME_DRIVER = chrome_driver