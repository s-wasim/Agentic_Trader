""" TODO:
    - Copy processed data to store in a structured DB
    - Add capability to switch to a Vector DB
"""

class BaseProcessor:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        self.main(*args, **kwargs)