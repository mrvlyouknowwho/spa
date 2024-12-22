# config.py
import os

class Config:
    def __init__(self):
        print("Config: Инициализация")
        self.debug_mode = True
        self.db_name = "spa_data.db"
        self.log_file = "spa.log"
        self.parser_rules = "parser_rules.json"
        self.headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.internet_check_urls = ["https://www.google.com", "https://www.bing.com", "https://www.duckduckgo.com"]
        self.nlp_model_name = "bert-base-uncased"

    def get_config(self):
        return self.__dict__