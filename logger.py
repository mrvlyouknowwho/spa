# logger.py
import logging
import os
from config import Config

class Logger:
    def __init__(self, config):
        print("Logger: Инициализация")
        self.config = config
        self.logger = logging.getLogger("SPA")
        self.logger.setLevel(logging.DEBUG if self.config.debug_mode else logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Ensure log directory exists
        log_dir = os.path.dirname(self.config.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(self.config.log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def debug(self, message):
      if self.config.debug_mode:
        self.logger.debug(message)

    def info(self, message):
      self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)