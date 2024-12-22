# modules/self_analysis.py
import ast
import inspect
import os
import hashlib

class SelfAnalysis:
    def __init__(self):
        print("SelfAnalysis: Инициализация")
        self.memory = None
        self.user_interactions = []

    def set_memory(self, memory):
      print("SelfAnalysis: Установка памяти.")
      self.memory = memory

    def record_interaction(self, query, result):
        print(f"SelfAnalysis: Запись взаимодействия: запрос='{query}', результат='{result}'")
        self.user_interactions.append({"query": query, "result": result})
        if self.memory:
            self.memory.update_memory("past_actions", self.user_interactions)
        else:
            print("SelfAnalysis: Память не установлена, запись взаимодействия невозможна.")

    def analyze(self, module_name="self"):
        try:
            if module_name == "self":
                file_path = "modules/self_analysis.py"
            else:
                file_path = f"modules/{module_name}.py"
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            tree = ast.parse(code)
            errors = []
            suggestions = []
            hashes = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) == 0:
                        errors.append(f"Функция {node.name} пустая.")
                    if node.name == "__init__" and not any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and n.value.value == "self.memory = None" for n in node.body):
                        errors.append(f"Функция {node.name} не инициализирует self.memory.")
                    if node.name.startswith("handle_") and not any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == "append" for n in node.body):
                        suggestions.append(f"Функция {node.name} не выводит результат.")
                    code_hash = hashlib.sha256(ast.unparse(node).encode()).hexdigest()
                    if code_hash in hashes:
                        suggestions.append(f"Функция {node.name} дублирует код функции {hashes[code_hash]}.")
                    else:
                        hashes[code_hash] = node.name
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    if node.id.startswith("_"):
                        suggestions.append(f"Переменная {node.id} начинается с '_', что может указывать на неиспользуемую переменную.")
            if errors:
              print(f"SelfAnalysis: Обнаружены ошибки: {errors}, предложения: {suggestions}")
              return f"Обнаружены ошибки в коде:\n{', '.join(errors)}\nПредложения:\n{', '.join(suggestions)}"
            elif suggestions:
              print(f"SelfAnalysis: Код не содержит ошибок, но есть предложения: {suggestions}")
              return f"Код не содержит ошибок, но есть предложения:\n{', '.join(suggestions)}"
            else:
                print(f"SelfAnalysis: Код не содержит ошибок и предложений")
                return "Код не содержит ошибок и предложений."
        except FileNotFoundError:
            print(f"SelfAnalysis: Модуль не найден: {module_name}")
            return f"Модуль {module_name} не найден."
        except Exception as e:
          print(f"SelfAnalysis: Ошибка анализа кода: {e}")
          return f"Ошибка при анализе кода: {e}"

    def get_feedback(self, feedback):
      print(f"SelfAnalysis: Получена обратная связь: {feedback}")
      if self.memory:
        notes = self.memory.get_memory("notes") if self.memory.get_memory("notes") else []
        self.memory.update_memory("notes", notes + [feedback])
        print(f"SelfAnalysis: Обратная связь записана в память: {feedback}")
        return "Обратная связь получена."
      else:
        print("SelfAnalysis: Память не установлена, обратная связь не может быть записана.")
        return "Обратная связь получена, но память не установлена."