# modules/self_learning.py
import re
import random
from modules.search import Search

class SelfLearning:
    def __init__(self):
      print("SelfLearning: Инициализация")
      self.memory = None
      self.search = Search()

    def set_memory(self, memory):
        print("SelfLearning: Установка памяти")
        self.memory = memory

    def learn(self):
        print("SelfLearning: Начало процесса обучения")
        if not self.memory:
            print("SelfLearning: Память не установлена, обучение невозможно.")
            return "Память не установлена."
        past_actions = self.memory.get_memory("past_actions")
        if not past_actions:
            print("SelfLearning: Нет данных для обучения.")
            return "Нет данных для обучения."

        last_interaction = past_actions[-1]
        query = last_interaction["action"]
        result, error = last_interaction.get("result"), last_interaction.get("error")
        
        if error:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Ошибка: {query}, причина: {error}"])
            print(f"SelfLearning: Записал ошибку: {query}, причина: {error}")
            if "калькулятор" in query:
              self.learn_calculator(query, error)
            elif "поиск" in query:
               self.learn_search(query, error)
            return f"Записал ошибку и начал обучение: {query}, причина: {error}"
        
        if "неизвестно" in query:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Неизвестный запрос: {query}"])
            print(f"SelfLearning: Записал неизвестный запрос: {query}")
            self.learn_parser(query)
            return f"Записал неизвестный запрос и начал обучение парсера: {query}"
        if "код" in query:
            print(f"SelfLearning: Начал обучение движка на запросе: {query}")
            self.learn_engine(query)
            return f"Начал обучение движка на запросе: {query}"
        
        if result == "OK":
           notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
           self.memory.update_memory("notes", notes + [f"Успешное выполнение запроса: {query}"])
           print(f"SelfLearning: Записал успешное выполнение запроса: {query}")
           self.learn_memory(query)
           return f"Записал успешное выполнение запроса и начал обучение: {query}"
        
        print("SelfLearning: Обучение пока не реализовано.")
        return "Обучение пока не реализовано."

    def learn_parser(self, query):
        if not self.memory:
            print("SelfLearning: Память не установлена, обучение парсера невозможно.")
            return "Память не установлена."
        parser = self.memory.get_memory("modules.parser")
        if not parser:
            print("SelfLearning: Модуль парсера не найден, обучение невозможно.")
            return "Модуль парсера не найден."
        
        query = query.lower()
        words = query.split()
        if "поиск" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["поиск"])
            print("SelfLearning: Парсер обучен на поиск.")
        elif "калькулятор" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["калькулятор"])
            print("SelfLearning: Парсер обучен на калькулятор.")
        elif "код" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["код"])
            print("SelfLearning: Парсер обучен на код.")
        elif "обучение" in words or "python" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["обучение"])
            print("SelfLearning: Парсер обучен на обучение.")
        elif "интерфейс" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["интерфейс"])
            print("SelfLearning: Парсер обучен на интерфейс.")
        elif "файл" in words or "pdf" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["файл"])
            print("SelfLearning: Парсер обучен на файл.")
        elif "память" in words:
            tasks = self.memory.get_memory("modules.parser.tasks") if self.memory.get_memory("modules.parser.tasks") else []
            self.memory.update_memory("modules.parser.tasks", tasks + ["память"])
            print("SelfLearning: Парсер обучен на память.")
        else:
            new_rule = re.escape(query)
            parser_object = self.memory.get_memory("modules.parser")
            if parser_object:
                parser_object.add_rule(new_rule, query.split()[0])
                self.memory.update_memory("modules.parser", parser_object)
                notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
                self.memory.update_memory("notes", notes + [f"Добавлено новое правило парсера: {query} -> {query.split()[0]}"])
                print(f"SelfLearning: Парсер обучен на запросе: {query}")
                return f"Парсер обучен на запросе: {query}"
            else:
                print("SelfLearning: Модуль парсера не найден, обучение невозможно.")
                return "Модуль парсера не найден."
    def learn_engine(self, query):
        if not self.memory:
            print("SelfLearning: Память не установлена, обучение движка невозможно.")
            return "Память не установлена."
        engine = self.memory.get_memory("modules.engine")
        if not engine:
            print("SelfLearning: Модуль движка не найден, обучение невозможно.")
            return "Модуль движка не найден."
        
        tasks = self.memory.get_memory("modules.engine.tasks") if self.memory.get_memory("modules.engine.tasks") else []
        self.memory.update_memory("modules.engine.tasks", tasks + [query])
        print(f"SelfLearning: Движок обучен на запросе: {query}")
        return f"Движок обучен на запросе: {query}"
    
    def learn_calculator(self, query, error):
         if "Некорректное выражение" in error:
           notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
           self.memory.update_memory("notes", notes + [f"Некорректное выражение калькулятора: {query}"])
           print(f"SelfLearning: Записал ошибку калькулятора: {query}")
           parser = self.memory.get_memory("modules.parser")
           if parser:
               new_rule = re.escape(query)
               parser.add_rule(new_rule, "калькулятор")
               self.memory.update_memory("modules.parser", parser)
               notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
               self.memory.update_memory("notes", notes + [f"Добавлено новое правило парсера для калькулятора: {query} -> калькулятор"])
               print(f"SelfLearning: Парсер обучен на запросе калькулятора: {query}")
           else:
                print("SelfLearning: Модуль парсера не найден, обучение невозможно.")
                return "Модуль парсера не найден."
    def learn_search(self, query, error):
       if "Нет подключения к интернету" in error:
           notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
           self.memory.update_memory("notes", notes + [f"Ошибка поиска: нет подключения к интернету"])
           print(f"SelfLearning: Записал ошибку поиска: нет подключения к интернету.")
           
           search = self.memory.get_memory("modules.search")
           if search:
               if search.current_engine == "duckduckgo":
                 search.set_search_engine("google")
                 self.memory.update_memory("modules.search", search)
                 notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
                 self.memory.update_memory("notes", notes + [f"Поменял поисковую систему на google."])
                 print("SelfLearning: Поменял поисковую систему на google")
               elif search.current_engine == "google":
                 search.set_search_engine("bing")
                 self.memory.update_memory("modules.search", search)
                 notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
                 self.memory.update_memory("notes", notes + [f"Поменял поисковую систему на bing."])
                 print("SelfLearning: Поменял поисковую систему на bing")
               elif search.current_engine == "bing":
                 search.set_search_engine("duckduckgo")
                 self.memory.update_memory("modules.search", search)
                 notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
                 self.memory.update_memory("notes", notes + [f"Поменял поисковую систему на duckduckgo."])
                 print("SelfLearning: Поменял поисковую систему на duckduckgo")
           else:
                print("SelfLearning: Модуль поиска не найден, обучение невозможно.")
                return "Модуль поиска не найден."
       elif "Ошибка поиска" in error:
           notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
           self.memory.update_memory("notes", notes + [f"Ошибка поиска: {query}"])
           print(f"SelfLearning: Записал ошибку поиска: {query}")
           parser = self.memory.get_memory("modules.parser")
           if parser:
               new_rule = re.escape(query)
               parser.add_rule(new_rule, "поиск")
               self.memory.update_memory("modules.parser", parser)
               notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
               self.memory.update_memory("notes", notes + [f"Добавлено новое правило парсера для поиска: {query} -> поиск"])
               print(f"SelfLearning: Парсер обучен на запросе поиска: {query}")
           else:
                print("SelfLearning: Модуль парсера не найден, обучение невозможно.")
                return "Модуль парсера не найден."
    
    def learn_memory(self, query):
        if not self.memory:
            print("SelfLearning: Память не установлена, обучение памяти невозможно.")
            return "Память не установлена."
        
        memory = self.memory.get_memory("modules.memory")
        if not memory:
            print("SelfLearning: Модуль памяти не найден, обучение невозможно.")
            return "Модуль памяти не найден."
        
        if "сохранить" in query:
          notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
          self.memory.update_memory("notes", notes + [f"Успешный запрос на сохранение памяти: {query}"])
          print(f"SelfLearning: Записал успешный запрос на сохранение памяти: {query}")
        elif "загрузить" in query:
          notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
          self.memory.update_memory("notes", notes + [f"Успешный запрос на загрузку памяти: {query}"])
          print(f"SelfLearning: Записал успешный запрос на загрузку памяти: {query}")
        elif "поиск" in query:
           notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
           self.memory.update_memory("notes", notes + [f"Успешный запрос на поиск в памяти: {query}"])
           print(f"SelfLearning: Записал успешный запрос на поиск в памяти: {query}")
        elif "анализ" in query:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Успешный запрос на анализ памяти: {query}"])
            print(f"SelfLearning: Записал успешный запрос на анализ памяти: {query}")
        elif "план" in query:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Успешный запрос на планирование памяти: {query}"])
            print(f"SelfLearning: Записал успешный запрос на планирование памяти: {query}")
        elif "обновить" in query:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Успешный запрос на обновление памяти: {query}"])
            print(f"SelfLearning: Записал успешный запрос на обновление памяти: {query}")
        elif "получить" in query:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Успешный запрос на получение данных из памяти: {query}"])
            print(f"SelfLearning: Записал успешный запрос на получение данных из памяти: {query}")
        elif "очистить" in query:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Успешный запрос на очистку памяти: {query}"])
            print(f"SelfLearning: Записал успешный запрос на очистку памяти: {query}")
        else:
            notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
            self.memory.update_memory("notes", notes + [f"Успешный запрос к памяти: {query}"])
            print(f"SelfLearning: Записал успешный запрос к памяти: {query}")