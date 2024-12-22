import re
import json
import os

class Parser:
    def __init__(self):
        self.history = []
        self.rules = self.load_rules()

    def parse_query(self, text):
        self.history.append(text)
        text = text.lower()
        
        for rule, action in self.rules.items():
             match = re.search(rule, text)
             if match:
                  return action, match.groups() if match.groups() else []
             
        if "создай калькулятор" in text:
            return "калькулятор", []
        elif re.search(r"создай калькулятор\s*(.+)", text):
            return "калькулятор", re.search(r"создай калькулятор\s*(.+)", text).groups()
        elif "проанализируй свой код" in text:
            return "код", ["анализ"]
        elif "обучи меня пайтону" in text:
            return "обучение", []
        elif re.search(r"(?:создай|сделай) кнопку\s*(?:с именем)?\s*(.+)?", text):
             return "интерфейс", text.split()
        elif "создай поле ввода" in text or "создай текстовое поле" in text or "создай выпадающий список" in text or "измени текст кнопки" in text:
            return "интерфейс", text.split()
        elif re.search(r"(?:загрузи|открой)\s*(?:файл|книгу)\s*(.+)?", text):
            return "файл", text.split()
        elif "сохранить память" in text or "загрузить память" in text or "поиск в памяти" in text or "анализ памяти" in text or "план действий" in text or "обновить память" in text or "получить из памяти" in text or "очистить память" in text:
            return "память", text.split()
        elif "напиши" in text and "калькулятор" in text:
            return "поиск", text.split()
        else:
            return "поиск", text.split()
    
    def add_rule(self, rule, action):
        self.rules[rule] = action
        self.save_rules()
        
    def load_rules(self):
        if os.path.exists("parser_rules.json"):
            with open("parser_rules.json", "r") as f:
                return json.load(f)
        return {}

    def save_rules(self):
        with open("parser_rules.json", "w") as f:
            json.dump(self.rules, f, indent=4)

    def get_history(self):
        return self.history