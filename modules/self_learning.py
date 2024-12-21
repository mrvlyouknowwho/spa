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
        # Здесь будет логика обучения
        return "Обучение пока не реализовано."