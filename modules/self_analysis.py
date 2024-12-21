import ast
import inspect

class SelfAnalysis:
    def __init__(self):
        self.memory = None
        self.user_interactions = []

    def set_memory(self, memory):
        self.memory = memory

    def record_interaction(self, query, result):
        self.user_interactions.append({"query": query, "result": result})
        self.memory.update_memory("past_actions", self.user_interactions)

    def analyze(self):
        try:
            with open("modules/self_analysis.py", "r", encoding="utf-8") as f:
                code = f.read()
            tree = ast.parse(code)
            errors = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) == 0:
                        errors.append(f"Функция {node.name} пустая.")
                    if node.name == "__init__" and not any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and n.value.value == "self.memory = None" for n in node.body):
                        errors.append(f"Функция {node.name} не инициализирует self.memory.")
            if errors:
                return f"Обнаружены ошибки в коде:\n{', '.join(errors)}"
            else:
                return "Код не содержит ошибок."
        except Exception as e:
            return f"Ошибка при анализе кода: {e}"

    def get_feedback(self, feedback):
        # Здесь будет логика обработки обратной связи
        self.memory.update_memory("notes", self.memory.get_memory("notes") + [feedback])
        return "Обратная связь получена."