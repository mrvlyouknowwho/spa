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
            return f"Записал неизвестный запрос: {query}"
        return "Обучение пока не реализовано."