""" TODO:
    - Copy processed data to store in a structured DB
    - Add capability to switch to a Vector DB
"""
from helpers import Logger

class BaseProcessor:
    def __init__(self):
        _ = Logger(type(self).__name__)
        self.log = _.logger

    def __call__(self, *args, **kwargs):
        self.main(*args, **kwargs)