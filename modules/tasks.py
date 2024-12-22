import re
import random
# try:
#     from googletrans import Translator
# except ImportError:
#     print("Модуль googletrans не установлен. Пожалуйста, установите его с помощью команды: pip install googletrans==4.0.0-rc1")
#     Translator = None
Translator = None

class Tasks:
    def __init__(self):
        if Translator:
            self.translator = Translator()
        else:
            self.translator = None

    def create_calculator(self, expression):
        try:
            if not expression:
              return "Некорректное выражение."
            expression = expression.replace(" ", "")
            if re.match(r"^[0-9+\-*/().]+$", expression):
                result = eval(expression)
                return result
            else:
                return "Некорректное выражение."
        except Exception as e:
            return f"Ошибка вычисления: {e}"

    def analyze_text(self, text):
        words = text.lower().split()
        word_count = len(words)
        unique_words = len(set(words))
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len(sentences) - 1 if sentences[-1] == '' else len(sentences)
        return f"Анализ текста:\nСлов: {word_count}\nУникальных слов: {unique_words}\nПредложений: {sentence_count}"

    def automate_action(self, action):
        if action == "случайное число":
            return random.randint(1, 100)
        else:
            return "Автоматизация действия пока не реализована."

    def translate_text(self, text, dest_lang="en"):
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
        # Здесь будет логика поиска синонимов
        return "Поиск синонимов пока не реализован."