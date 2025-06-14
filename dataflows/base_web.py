class BaseWebDriver():
    def __init__(self, driver_option):
        # Setup Chrome options
        self.driver = driver_option

    def __enter__(self):
        print('Web driver instantiated properly')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Destroying Web Driver')
        self.driver.quit()
        print('Web Driver Destroyed')
