import json
import random
import heapq
import os

from modules.database import DatabaseManager

class Memory:
    def __init__(self):
        self.db = DatabaseManager()
        self.data = {}
        self.instructions = self._load_instructions()
        self._load_initial_data()
      
    def _load_instructions(self):
        instructions = {
            "restore_state": "Для восстановления состояния после перезапуска, загрузите сохраненную память.",
            "memory_format": "Память хранится в формате JSON.",
            "weight_algorithm": "Веса элементов памяти динамически изменяются в зависимости от их использования.",
            "learning_algorithm": "Самообучение происходит на основе данных о взаимодействии с пользователем.",
            "parser_tasks": "Парсер обучается на новых запросах, которые он не понимает.",
            "engine_tasks": "Движок обучается на новых данных, которые он получает от пользователя."
        }
        return instructions
      
    def _load_initial_data(self):
      initial_data = {
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
          }
        }
      self.data = initial_data
      
    def save_memory(self):
       for key, value in self.data.items():
           self.db.save_data(key, value)
       return json.dumps(self.data, separators=(',', ':'))
       
    def add_past_action(self, timestamp, action, result):
      self.db.add_past_action(timestamp, action, result)
    
    def get_past_actions(self):
      return self.db.get_past_actions()
    
    def update_memory(self, key, value):
        parts = key.split('.')
        current = self.data
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    
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
      return "Анализ памяти пока не реализован."

    def plan_actions(self):
        return "Планирование действий пока не реализовано."

    def update_weights(self, key):
        if not hasattr(self, 'weights'):
            self.weights = {}
        if key not in self.weights:
            self.weights[key] = 0.5
        self.weights[key] += random.uniform(0.1, 0.3)
        for k in self.weights:
            if k != key:
                self.weights[k] *= 0.9
        self.normalize_weights()

    def get_weight(self, key):
      if not hasattr(self, 'weights'):
            self.weights = {}
      return self.weights.get(key, 0.1)

    def normalize_weights(self):
      if not hasattr(self, 'weights'):
            self.weights = {}
      total_weight = sum(self.weights.values())
      if total_weight > 0:
        for key in self.weights:
          self.weights[key] /= total_weight