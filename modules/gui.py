from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QComboBox, QLabel)
from PyQt6.QtCore import Qt
from modules.parser import Parser
from modules.search import Search
from modules.engine import Engine
from modules.tasks import Tasks
from modules.self_analysis import SelfAnalysis
from modules.files import Files
from modules.memory import Memory

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самообучающийся Персональный Ассистент (СПА)")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Введите запрос...")
        self.layout.addWidget(self.query_input)

        self.execute_button = QPushButton("Выполнить")
        self.execute_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.execute_button)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.layout.addWidget(self.result_output)

        # Инициализация модулей
        self.memory = Memory()
        self.parser = Parser()
        self.parser.set_memory(self.memory)
        self.search = Search()
        self.engine = Engine()
        self.tasks = Tasks()
        self.self_analysis = SelfAnalysis()
        self.self_analysis.set_memory(self.memory)
        self.files = Files()

    def execute_query(self):
        query = self.query_input.text()
        self.result_output.append(f"Запрос: {query}\n")
        query_type, words = self.parser.parse_query(query)

        if query_type == "поиск":
            self.handle_search(words)
        elif query_type == "калькулятор":
            self.handle_calculator(words)
        elif query_type == "код":
            self.handle_code(words)
        elif query_type == "обучение":
            self.handle_learning(words)
        elif query_type == "интерфейс":
            self.handle_interface(words)
        elif query_type == "файл":
            self.handle_file(words)
        elif query_type == "память":
            self.handle_memory(words)
        else:
            self.result_output.append("Неизвестный запрос.\n")
        self.self_analysis.record_interaction(query, "OK")

    def handle_search(self, words):
        search_query = " ".join(words[1:])
        results = self.search.search_internet(search_query)
        if isinstance(results, str):
            self.result_output.append(results + "\n")
        else:
            self.result_output.append("Результаты поиска:\n")
            for result in results:
                self.result_output.append(f"{result['title']}: {result['url']}\n")
                self.extract_text_from_url(result['url'])

    def extract_text_from_url(self, url):
        text = self.search.extract_text_from_url(url)
        if isinstance(text, str):
            self.result_output.append(f"Текст со страницы {url}:\n{text[:500]}...\n")
        else:
            self.result_output.append(f"Ошибка при извлечении текста: {text}\n")

    def handle_calculator(self, words):
        expression = " ".join(words[1:])
        result = self.tasks.create_calculator(expression)
        self.result_output.append(f"Результат: {result}\n")

    def handle_code(self, words):
        prompt = " ".join(words[1:])
        generated_code = self.engine.generate_text(prompt)
        self.result_output.append(f"Сгенерированный код:\n{generated_code}\n")

    def handle_learning(self, words):
        search_query = " ".join(words[1:]) + " обучение python"
        results = self.search.search_internet(search_query)
        if isinstance(results, str):
            self.result_output.append(results + "\n")
        else:
            self.result_output.append("Результаты поиска по обучению Python:\n")
            for result in results:
                self.result_output.append(f"{result['title']}: {result['url']}\n")

    def handle_interface(self, words):
        if "кнопку" in words:
            self.create_button()
        elif "поле ввода" in words:
            self.create_input_field()
        elif "текстовое поле" in words:
            self.create_text_field()
        elif "выпадающий список" in words:
            self.create_combo_box()
        else:
            self.result_output.append("Неизвестный запрос интерфейса.\n")

    def create_button(self):
        button = QPushButton("Новая кнопка")
        button.clicked.connect(lambda: self.result_output.append("Кнопка нажата!\n"))
        self.layout.addWidget(button)
        self.result_output.append("Кнопка создана.\n")

    def create_input_field(self):
        input_field = QLineEdit()
        input_field.setPlaceholderText("Введите текст...")
        self.layout.addWidget(input_field)
        self.result_output.append("Поле ввода создано.\n")

    def create_text_field(self):
        text_field = QTextEdit()
        text_field.setReadOnly(True)
        self.layout.addWidget(text_field)
        self.result_output.append("Текстовое поле создано.\n")

    def create_combo_box(self):
        combo_box = QComboBox()
        combo_box.addItems(["Пункт 1", "Пункт 2", "Пункт 3"])
        self.layout.addWidget(combo_box)
        self.result_output.append("Выпадающий список создан.\n")

    def handle_file(self, words):
        if "загрузить" in words:
            self.load_file()
        elif "сохранить" in words:
            self.save_file()

    def load_file(self):
        file_path = self.files.load_file()
        if file_path:
            text = self.files.extract_text_from_pdf(file_path)
            self.result_output.append(f"Текст из PDF {file_path}:\n{text[:500]}...\n")

    def save_file(self):
        text_to_save = self.result_output.toPlainText()
        result = self.files.save_file(text_to_save)
        if result:
            self.result_output.append(result + "\n")

    def handle_memory(self, words):
        if "сохранить" in words:
            memory_data = self.memory.save_memory()
            self.result_output.append(f"Память сохранена:\n{memory_data}\n")
        elif "загрузить" in words:
            # Здесь будет логика загрузки памяти
            self.result_output.append("Загрузка памяти пока не реализована.\n")
        elif "поиск" in words:
            search_query = " ".join(words[1:])
            results = self.memory.search_memory(search_query)
            self.result_output.append(f"Результаты поиска в памяти:\n{results}\n")
        elif "анализ" in words:
            analysis = self.memory.analyze_memory()
            self.result_output.append(f"Анализ памяти:\n{analysis}\n")
        elif "план" in words:
            plan = self.memory.plan_actions()
            self.result_output.append(f"План действий:\n{plan}\n")
        elif "обновить" in words:
            key = words[2]
            value = " ".join(words[3:])
            self.memory.update_memory(key, value)
            self.result_output.append(f"Память обновлена: {key} = {value}\n")
        elif "получить" in words:
            key = " ".join(words[2:])
            value = self.memory.get_memory(key)
            self.result_output.append(f"Значение из памяти: {key} = {value}\n")
        else:
            self.result_output.append("Неизвестный запрос памяти.\n")