import time
import re

from helpers.env_vars import ENV_VARS
from dataflows.helper.web_drivers import WEB_DRIVERS
from dataflows.base_web import BaseWebDriver

class SarmayaDataflow(BaseWebDriver):
    def __init__(self):
        super().__init__(
            WEB_DRIVERS.CHROME_DRIVER(
                driver_path=ENV_VARS.CHROME_WEB_DRIVER_PATH.value
                )
            )
        self.base_url = 'https://sarmaaya.pk/'

    def get_page_detail(self, extension_url, data_gate_id):
        shariah_link = f'{self.base_url}{extension_url}'
        # Get page
        self.driver.get(shariah_link)
        time.sleep(2)
        return [*map(
            lambda x: (x.split('/')[-1], x), 
            [
                re.search(pattern=r'<a href="(.*?)"', string=elem[0]).group(1)
                for elem in self.driver.execute_script(f"return $('#{data_gate_id}').DataTable().data().toArray()")
            ]
        )]


if __name__ == "__main__":
    with SarmayaDataflow() as dataflow:
        _list = dataflow.get_page_detail(extension_url='psx/market/KMIALLSHR', data_gate_id='stock-screener')
    print(*_list, sep='\n')