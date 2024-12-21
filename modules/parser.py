import re
import json
import os

class Parser:
    def __init__(self):
        self.history = []
        self.rules = {}  # Инициализируем rules как пустой словарь

    def parse(self, text):
        self.history.append(text)
        text = text.lower()

        for rule, action in self.rules.items():
            if re.search(rule, text):
                return action

        if "создай калькулятор" in text:
            return "create_calculator"
        elif "проанализируй свой код" in text:
            return "analyze_code"
        elif "обучи меня пайтону" in text:
            return "learn_python"
        else:
            return "search_internet"

    def add_rule(self, rule, action):
        self.rules[rule] = action
        # TODO: Реализовать сохранение правил в файл parser_rules.json

    def get_history(self):
        return self.history