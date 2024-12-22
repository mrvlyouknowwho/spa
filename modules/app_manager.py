# modules/app_manager.py
import datetime
from modules.parser import Parser
from modules.search import Search
from modules.engine import Engine
from modules.tasks import Tasks
from modules.self_analysis import SelfAnalysis
from modules.files import Files
from modules.memory import Memory

class AppManager:
    def __init__(self, memory, debug_callback):
        print("AppManager: Инициализация - Начало")
        self.memory = memory # Используем переданный объект memory
        print("AppManager: Инициализирована Memory")
        print("AppManager: Инициализация Parser - Начало")
        self.parser = Parser()
        print("AppManager: Инициализирован Parser - Конец")
        print("AppManager: Инициализация Search - Начало")
        self.search = Search()
        print("AppManager: Инициализирован Search - Конец")
        print("AppManager: Инициализация Engine - Начало")
        self.engine = Engine()
        print("AppManager: Инициализирован Engine - Конец")
        print("AppManager: Инициализация Tasks - Начало")
        self.tasks = Tasks()
        print("AppManager: Инициализирован Tasks - Конец")
        print("AppManager: Инициализация SelfAnalysis - Начало")
        self.self_analysis = SelfAnalysis()
        print("AppManager: Инициализирован SelfAnalysis - Конец")
        self.self_analysis.set_memory(self.memory)
        print("AppManager: Инициализация Files - Начало")
        self.files = Files()
        print("AppManager: Инициализирован Files - Конец")
        self.debug_callback = debug_callback
        print("AppManager: Инициализация - Конец")
    
    def execute_query(self, query):
        self.debug_callback(f"AppManager: Запрос: {query}", 'app_manager')
        query_type, words = self.parser.parse_query(query)
        self.debug_callback(f"AppManager: Парсер: {query_type}, {words}", 'app_manager')
        
        if query_type == "поиск":
          return "search", {'query':" ".join(words[1:])}
        elif query_type == "калькулятор":
          if words:
             return "calculator", " ".join(words[1:])
          else:
             return "calculator", None
        elif query_type == "код":
          return "code", words
        elif query_type == "обучение":
          return "learning", words
        elif query_type == "интерфейс":
          return "interface", words
        elif query_type == "файл":
          return "file", words
        elif query_type == "память":
          return "memory", words
        else:
          return "unknown", None
    
    def handle_code(self, words):
      prompt = " ".join(words[1:])
      self.debug_callback(f"AppManager: handle_code: Запрос: {prompt}", 'app_manager')
      generated_code = self.engine.generate_text(prompt)
      self.debug_callback(f"AppManager: handle_code: Сгенерированный код:\n{generated_code}", 'app_manager')
      return generated_code

    def handle_learning(self, words):
      search_query = " ".join(words[1:]) + " обучение python"
      self.debug_callback(f"AppManager: handle_learning: Запрос {search_query}", 'app_manager')
      try:
          results = self.search.search_internet(search_query)
          if isinstance(results, str):
              self.debug_callback(f"AppManager: handle_learning: Результаты поиска по обучению Python: {results}", 'app_manager')
          else:
              self.debug_callback(f"AppManager: handle_learning: Результаты поиска по обучению Python: {results}", 'app_manager')
          return results
      except Exception as e:
          self.debug_callback(f"AppManager: handle_learning: Ошибка: {e}", 'app_manager')
          return f"Ошибка поиска: {e}"

    def handle_interface(self, words):
        if "кнопку" in words:
           return "create_button", None
        elif "поле ввода" in words:
            return "create_input_field", None
        elif "текстовое поле" in words:
            return "create_text_field", None
        elif "выпадающий список" in words:
            return "create_combo_box", None
        elif "изменить текст кнопки" in words:
            return "change_button_text", words
        else:
           self.debug_callback(f"AppManager: handle_interface: Неизвестный запрос интерфейса: {words}", 'app_manager')
           return "unknown", None

    def handle_file(self, words):
        if "загрузить" in words:
           return "load_file", None
        elif "сохранить" in words:
            return "save_file", None

    def handle_memory(self, words):
      if "сохранить" in words:
        return "save_memory", None
      elif "загрузить" in words:
        return "load_memory", None
      elif "поиск" in words:
        return "search_memory", " ".join(words[1:])
      elif "анализ" in words:
        return "analyze_memory", None
      elif "план" in words:
        return "plan_memory", None
      elif "обновить" in words:
          return "update_memory",  {"key":words[2], "value": " ".join(words[3:])}
      elif "получить" in words:
          return "get_memory", " ".join(words[2:])
      elif "очистить" in words:
          return "clear_memory", None
      else:
        self.debug_callback(f"AppManager: handle_memory: Неизвестный запрос памяти.", 'app_manager')
        return "unknown", None

    def record_interaction(self, query, result):
      self.memory.record_interaction(query, result)