""" TODO:
    - Copy processed data to store in a structured DB
    - Add capability to switch to a Vector DB
"""
from airflow.utils.log.logging_mixin import LoggingMixin

class BaseProcessor(LoggingMixin):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        self.main(*args, **kwargs)