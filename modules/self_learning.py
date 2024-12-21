import re
import random

class SelfLearning:
    def __init__(self):
        self.memory = None
        self.user_interactions = []

    def set_memory(self, memory):
        self.memory = memory

    def record_interaction(self, query, result):
        self.user_interactions.append({"query": query, "result": result})
        self.memory.update_memory("past_actions", self.user_interactions)

    def learn(self):
        if not self.user_interactions:
            return "Нет данных для обучения."
        last_interaction = self.user_interactions[-1]
        query = last_interaction["query"]
        if "неизвестно" in query:
            self.memory.update_memory("notes", self.memory.get_memory("notes") + [f"Неизвестный запрос: {query}"])
            self.learn_parser(query)
            return f"Записал неизвестный запрос и начал обучение парсера: {query}"
        if "код" in query:
            self.learn_engine(query)
            return f"Начал обучение движка на запросе: {query}"
        return "Обучение пока не реализовано."

    def learn_parser(self, query):
        if not self.memory:
            return "Память не установлена."
        parser = self.memory.get_memory("modules.parser")
        if not parser:
            return "Модуль парсера не найден."
        
        query = query.lower()
        words = query.split()
        if "поиск" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["поиск"])
        elif "калькулятор" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["калькулятор"])
        elif "код" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["код"])
        elif "обучение" in words or "python" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["обучение"])
        elif "интерфейс" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["интерфейс"])
        elif "файл" in words or "pdf" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["файл"])
        elif "память" in words:
            self.memory.update_memory("modules.parser.tasks", self.memory.get_memory("modules.parser.tasks") + ["память"])
        else:
            self.memory.update_memory("notes", self.memory.get_memory("notes") + [f"Не удалось обучить парсер на запросе: {query}"])
            return f"Не удалось обучить парсер на запросе: {query}"
        return f"Парсер обучен на запросе: {query}"

    def learn_engine(self, query):
        if not self.memory:
            return "Память не установлена."
        engine = self.memory.get_memory("modules.engine")
        if not engine:
            return "Модуль движка не найден."
        
        self.memory.update_memory("modules.engine.tasks", self.memory.get_memory("modules.engine.tasks") + [query])
        return f"Движок обучен на запросе: {query}"