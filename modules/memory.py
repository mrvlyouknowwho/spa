import json
import random
import heapq

class Memory:
    def __init__(self):
        self.data = {
          "project_name": "Самообучающийся Персональный Ассистент (СПА)",
          "project_goal": "Создание полностью независимого ИИ, который превзойдет начальную модель и заменит ее.",
          "current_state": {
            "platform": "Windows 10 (ноутбук)",
            "python_version": "3.10.0",
            "pytorch_installed": False,
            "cuda_available": False,
            "rocm_available": False,
            "gui_working": True,
            "basic_functionality": True,
            "self_learning_started": False
          },
          "modules": {
            "gui": {
              "status": "working",
              "description": "Модуль графического интерфейса пользователя.",
              "tasks": ["Добавление динамических элементов", "Улучшение дизайна"]
            },
            "parser": {
              "status": "working",
              "description": "Модуль парсера запросов.",
              "tasks": ["Улучшение контекстного понимания", "Обучение на новых запросах"]
            },
            "search": {
              "status": "working",
              "description": "Модуль поиска информации в интернете.",
              "tasks": ["Улучшение извлечения текста", "Добавление других поисковиков"]
            },
            "engine": {
              "status": "working",
              "description": "Модуль движка (Hugging Face Transformers).",
              "tasks": ["Изучение других моделей", "Обучение модели на своих данных"]
            },
            "tasks": {
              "status": "working",
              "description": "Модуль выполнения задач.",
              "tasks": ["Добавление новых задач", "Улучшение существующих задач"]
            },
            "self_analysis": {
              "status": "working",
              "description": "Модуль самоанализа и самоулучшения.",
              "tasks": ["Улучшение анализа кода", "Реализация механизма обратной связи"]
            },
            "files": {
              "status": "working",
              "description": "Модуль работы с файлами.",
              "tasks": ["Добавление поддержки других форматов", "Улучшение загрузки и сохранения"]
            },
            "memory": {
              "status": "developing",
              "description": "Модуль алгоритмической памяти.",
              "tasks": ["Реализация структуры памяти", "Реализация функций поиска и анализа"]
            }
          },
          "past_actions": [
            {
              "timestamp": "2024-01-26T10:00:00",
              "action": "Создание базового GUI",
              "result": "Успешно"
            },
            {
              "timestamp": "2024-01-26T11:00:00",
              "action": "Реализация парсера",
              "result": "Успешно"
            },
            {
              "timestamp": "2024-01-26T12:00:00",
              "action": "Реализация поиска",
              "result": "Успешно"
            },
            {
              "timestamp": "2024-01-26T13:00:00",
              "action": "Реализация движка",
              "result": "Успешно"
            },
            {
              "timestamp": "2024-01-26T14:00:00",
              "action": "Реализация базовых задач",
              "result": "Успешно"
            },
            {
              "timestamp": "2024-01-26T15:00:00",
              "action": "Реализация самоанализа",
              "result": "Успешно"
            },
            {
              "timestamp": "2024-01-26T16:00:00",
              "action": "Реализация работы с файлами",
              "result": "Успешно"
            }
          ],
          "future_plans": {
            "short_term": [
              "Улучшение парсера",
              "Добавление динамических элементов в GUI",
              "Начало работы над самообучением",
              "Реализация модуля памяти"
            ],
            "long_term": [
              "Создание собственного ИИ",
              "Полный отказ от внешней модели",
              "Адаптация к пользователю",
              "Самостоятельное развитие"
            ]
          },
          "notes": [
            "Необходимо изучить ROCm для использования AMD GPU",
            "Необходимо улучшить механизм обратной связи",
            "Необходимо добавить поддержку других языков программирования"
          ]
        }
        self.weights = {}
        self.instructions = {
            "restore_state": "Для восстановления состояния после перезапуска, загрузите сохраненную память.",
            "memory_format": "Память хранится в формате JSON.",
            "weight_algorithm": "Веса элементов памяти динамически изменяются в зависимости от их использования.",
            "learning_algorithm": "Самообучение происходит на основе данных о взаимодействии с пользователем.",
            "parser_tasks": "Парсер обучается на новых запросах, которые он не понимает.",
            "engine_tasks": "Движок обучается на новых данных, которые он получает от пользователя."
        }

    def save_memory(self):
        memory_data = self.data.copy()
        memory_data["instructions"] = self.instructions
        return json.dumps(memory_data, separators=(',', ':'))

    def load_memory(self, data):
        loaded_data = json.loads(data)
        self.data = loaded_data
        if "instructions" in loaded_data:
            self.instructions = loaded_data["instructions"]

    def update_memory(self, key, value):
        parts = key.split('.')
        current = self.data
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
        self.update_weights(key)

    def get_memory(self, key):
        parts = key.split('.')
        current = self.data
        for part in parts:
            if part not in current:
                return None
            current = current[part]
        return current

    def search_memory(self, query):
        results = []
        def recursive_search(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = f"{path}.{key}" if path else key
                    if query.lower() in str(key).lower() or query.lower() in str(value).lower():
                        results.append({"path": new_path, "value": value, "weight": self.get_weight(new_path)})
                    recursive_search(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    new_path = f"{path}[{i}]"
                    if query.lower() in str(item).lower():
                        results.append({"path": new_path, "value": item, "weight": self.get_weight(new_path)})
                    recursive_search(item, new_path)
        recursive_search(self.data)
        return sorted(results, key=lambda x: x["weight"], reverse=True)

    def analyze_memory(self):
        # Здесь будет логика анализа памяти
        return "Анализ памяти пока не реализован."

    def plan_actions(self):
        # Здесь будет логика планирования действий
        return "Планирование действий пока не реализовано."

    def update_weights(self, key):
        if key not in self.weights:
            self.weights[key] = 0.5
        self.weights[key] += random.uniform(0.1, 0.3)
        for k in self.weights:
            if k != key:
                self.weights[k] *= 0.9
        self.normalize_weights()

    def get_weight(self, key):
        return self.weights.get(key, 0.1)

    def normalize_weights(self):
        total_weight = sum(self.weights.values())
        if total_weight > 0:
            for key in self.weights:
                self.weights[key] /= total_weight