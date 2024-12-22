# modules/tasks.py
import re
import random
import ast

# try:
#     from googletrans import Translator
# except ImportError:
#     print("Модуль googletrans не установлен. Пожалуйста, установите его с помощью команды: pip install googletrans==4.0.0-rc1")
#     Translator = None
Translator = None

class Tasks:
    def __init__(self):
        print("Tasks: Инициализация")
        if Translator:
            self.translator = Translator()
        else:
            self.translator = None

    def create_calculator(self, expression):
        print(f"Tasks: Вычисление выражения: {expression}")
        try:
            if not expression:
              print("Tasks: Некорректное выражение.")
              return "Некорректное выражение.", "Некорректное выражение"
            expression = expression.replace(" ", "")
            # if re.match(r"^[0-9+\-*/().]+$", expression):
            result = ast.literal_eval(expression)
            print(f"Tasks: Результат вычисления: {result}")
            return result, "ok"
            # else:
            #     print("Tasks: Некорректное выражение.")
            #     return "Некорректное выражение."
        except Exception as e:
            print(f"Tasks: Ошибка вычисления: {e}")
            return f"Ошибка вычисления: {e}", "Ошибка вычисления"

    def analyze_text(self, text):
        print(f"Tasks: Анализ текста: {text}")
        words = text.lower().split()
        word_count = len(words)
        unique_words = len(set(words))
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len(sentences) - 1 if sentences[-1] == '' else len(sentences)
        result = f"Анализ текста:\nСлов: {word_count}\nУникальных слов: {unique_words}\nПредложений: {sentence_count}"
        print(f"Tasks: Результат анализа: {result}")
        return result

    def automate_action(self, action):
        print(f"Tasks: Автоматизация действия: {action}")
        if action == "случайное число":
            result = random.randint(1, 100)
            print(f"Tasks: Результат автоматизации: {result}")
            return result
        else:
            print("Tasks: Автоматизация действия пока не реализована.")
            return "Автоматизация действия пока не реализована."

    def translate_text(self, text, dest_lang="en"):
        print(f"Tasks: Попытка перевода: {text} на {dest_lang}")
        return "Перевод текста не реализован"
      #   if self.translator:
      #       try:
      #           translation = self.translator.translate(text, dest=dest_lang)
      #           return translation.text
      #       except Exception as e:
      #           return f"Ошибка перевода: {e}"
      #   else:
      #       return "Модуль googletrans не установлен."

    def find_synonyms(self, word):
        print(f"Tasks: Поиск синонимов для слова: {word}")
        return "Поиск синонимов пока не реализован."