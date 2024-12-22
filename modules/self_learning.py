# modules/self_learning.py
import re
import random

class SelfLearning:
    def __init__(self):
      print("SelfLearning: Инициализация")
      self.memory = None
      self.user_interactions = []

    def set_memory(self, memory):
        print("SelfLearning: Установка памяти")
        self.memory = memory

    def record_interaction(self, query, result):
      print(f"SelfLearning: Запись взаимодействия: запрос='{query}', результат='{result}'")
      self.user_interactions.append({"query": query, "result": result})
      if self.memory:
        self.memory.update_memory("past_actions", self.user_interactions)
      else:
        print("SelfLearning: Память не установлена, запись взаимодействия невозможна.")

    def learn(self):
        print("SelfLearning: Начало процесса обучения")
        if not self.user_interactions:
            print("SelfLearning: Нет данных для обучения.")
            return "Нет данных для обучения."
        last_interaction = self.user_interactions[-1]
        query = last_interaction["query"]
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