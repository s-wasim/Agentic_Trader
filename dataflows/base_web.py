from helpers.env_vars import ENV_VARS
from dataflows.helper.web_drivers import WEB_DRIVERS

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

class BaseWebDriver():
    def __init__(self, driver_option):
        match driver_option:
            case 'chrome':
                driver = WEB_DRIVERS.CHROME_DRIVER(
                    '--log-level=3',
                    driver_path=ENV_VARS.CHROME_WEB_DRIVER_PATH.value,
                    option=ChromeOptions
                )
            case 'firefox':
                driver = WEB_DRIVERS.FIREFOX_DRIVER(
                    '--log-level=3',
                    driver_path=ENV_VARS.FIREFOX_WEB_DRIVER_PATH.value,
                    option=FirefoxOptions
                )
        # Setup driver options
        self.driver = driver

    def __enter__(self):
        print('Web driver instantiated properly')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Destroying Web Driver')
        self.driver.quit()
        print('Web Driver Destroyed')

    def __call__(self, *args, **kwargs):
        self.main(args, kwargs)
