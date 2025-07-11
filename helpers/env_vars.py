import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class ENV_VARS(Enum):
    CHROME_WEB_DRIVER_PATH = os.getenv('CHROME_WEB_DRIVER_PATH')
    FIREFOX_WEB_DRIVER_PATH = os.getenv('FIREFOX_WEB_DRIVER_PATH')