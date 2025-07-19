import logging
import sys

class LogFormatter(logging.Formatter):
    def __init__(self):
        # Configure logging
        super().__init__()
        self.formatters = {
            logging.DEBUG:    logging.Formatter('%(asctime)s - DEBUG - %(message)s'),
            logging.INFO:     logging.Formatter('%(asctime)s - INFO - %(message)s'),
            logging.WARNING:  logging.Formatter('%(asctime)s - WARNING - %(message)s [in %(filename)s:%(lineno)d]'),
            logging.ERROR:    logging.Formatter('%(asctime)s - ERROR - %(message)s [in %(filename)s:%(lineno)d]'),
            logging.CRITICAL: logging.Formatter('%(asctime)s - CRITICAL - %(message)s'),
        }

    def format(self, record):
        formatter = self.formatters.get(record.levelno, self.formatters[logging.INFO])
        return formatter.format(record)
    
class LogEmitter(logging.StreamHandler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        print(self.format(record))
    
class Logger:
    def __init__(self, logger_name):
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.DEBUG) # Capture all levels

        # Prevent duplicate handlers
        if self._logger.handlers:
            return
        formatter = LogFormatter()

        # --- Console Handler ---
        console_handler = LogEmitter()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    @property
    def logger(self):
        return self._logger