class Parser:
    def __init__(self):
        self.memory = None
        self.context = {}

    def set_memory(self, memory):
        self.memory = memory

    def parse_query(self, query):
        query = query.lower()
        words = query.split()
        if "поиск" in words:
            self.context["last_query_type"] = "поиск"
            return "поиск", words
        elif "калькулятор" in words:
            self.context["last_query_type"] = "калькулятор"
            return "калькулятор", words
        elif "код" in words:
            self.context["last_query_type"] = "код"
            return "код", words
        elif "обучение" in words or "python" in words:
            self.context["last_query_type"] = "обучение"
            return "обучение", words
        elif "интерфейс" in words:
            self.context["last_query_type"] = "интерфейс"
            return "интерфейс", words
        elif "файл" in words or "pdf" in words:
            self.context["last_query_type"] = "файл"
            return "файл", words
        elif "память" in words:
            self.context["last_query_type"] = "память"
            return "память", words
        elif "а" in words and self.context.get("last_query_type") == "поиск":
            return "поиск", words
        else:
            return "неизвестно", words

    def learn_query(self, query, query_type):
        # Здесь будет логика обучения парсера
        pass