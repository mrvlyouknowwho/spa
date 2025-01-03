# modules/parser.py
import re
import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from config import Config
from transformers import pipeline

class Parser:
    def __init__(self, memory):
        print("Parser: Инициализация")
        self.memory = memory
        self.history = []
        self.rules = self.load_rules()
        self.config = Config()
        try:
           nltk.data.find("tokenizers/punkt")
        except LookupError:
            print("Parser: Загрузка punkt tokenizer")
            nltk.download('punkt', quiet=True)
        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            print("Parser: Загрузка stopwords")
            nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('russian'))
        self.nlp_pipeline = pipeline("text-classification", model=self.config.nlp_model_name)
    
    def preprocess_text(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word.isalpha() and word not in self.stop_words]
        return " ".join(tokens)
    
    def analyze_sentiment(self, text):
      try:
        result = self.nlp_pipeline(text)[0]
        return result['label'], result['score']
      except Exception as e:
        print(f"Parser: Ошибка анализа тональности {e}")
        return None, None
    
    def parse_query(self, text):
        print(f"Parser: Парсинг запроса: {text}")
        self.history.append(text)
        preprocessed_text = self.preprocess_text(text)
        sentiment, score = self.analyze_sentiment(text)
        print(f"Parser: Тональность: {sentiment}, Оценка: {score}")
        text = text.lower()
        
        for rule, action in self.rules.items():
             match = re.search(rule, text)
             if match:
                  print(f"Parser: Найдено правило: {rule}, действие: {action}")
                  return action, match.groups() if match.groups() else []
             
        if "создай калькулятор" in text:
            print("Parser: Определено: калькулятор")
            return "калькулятор", []
        elif re.search(r"создай калькулятор\s*(.+)", text):
            print("Parser: Определено: калькулятор с параметрами")
            return "калькулятор", re.search(r"создай калькулятор\s*(.+)", text).groups()
        elif re.search(r"(\d+[\+\-\*\/]\d+)", text):
            print("Parser: Определено: калькулятор (выражение)")
            return "калькулятор", re.search(r"(\d+[\+\-\*\/]\d+)", text).groups()
        elif "проанализируй свой код" in text:
            print("Parser: Определено: код")
            return "код", ["анализ"]
        elif "обучи меня пайтону" in text:
             print("Parser: Определено: обучение")
             return "обучение", []
        elif re.search(r"(?:создай|сделай) кнопку\s*(?:с именем)?\s*(.+)?", text):
             print("Parser: Определено: интерфейс (кнопка)")
             return "интерфейс", text.split()
        elif "создай поле ввода" in text or "создай текстовое поле" in text or "создай выпадающий список" in text or "измени текст кнопки" in text:
            print("Parser: Определено: интерфейс (другой элемент)")
            return "интерфейс", text.split()
        elif re.search(r"(?:загрузи|открой)\s*(?:файл|книгу)\s*(.+)?", text):
            print("Parser: Определено: файл")
            return "файл", text.split()
        elif "сохранить память" in text or "загрузить память" in text or "поиск в памяти" in text or "анализ памяти" in text or "план действий" in text or "обновить память" in text or "получить из памяти" in text or "очистить память" in text:
            print("Parser: Определено: память")
            return "память", text.split()
        else:
            print("Parser: Определено: поиск")
            return "поиск", text.split()
    
    def add_rule(self, rule, action):
        print(f"Parser: Добавлено новое правило: {rule} -> {action}")
        self.rules[rule] = action
        self.save_rules()
        
    def load_rules(self):
        print("Parser: Загрузка правил парсера.")
        if os.path.exists("parser_rules.json"):
            with open("parser_rules.json", "r") as f:
                rules = json.load(f)
                print(f"Parser: Правила загружены: {rules}")
                return rules
        print("Parser: Файл с правилами не найден, загружены пустые правила.")
        return {}

    def save_rules(self):
        print(f"Parser: Сохранение правил: {self.rules}")
        with open("parser_rules.json", "w") as f:
            json.dump(self.rules, f, indent=4)

    def get_history(self):
        return self.history