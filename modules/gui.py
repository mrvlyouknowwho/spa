from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QComboBox, QLabel, QProgressBar, QHBoxLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from modules.parser import Parser
from modules.search import Search
from modules.engine import Engine
from modules.tasks import Tasks
from modules.self_analysis import SelfAnalysis
from modules.files import Files
from modules.memory import Memory
import json
import os
import datetime

class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    
    def __init__(self, task, parameters=None, debug_callback=None):
        super().__init__()
        self.task = task
        self.parameters = parameters
        self.is_running = True
        self.debug_callback = debug_callback
    
    def stop(self):
       self.is_running = False

    def run(self):
      if self.task == "search":
        if self.parameters and 'query' in self.parameters:
          for i in range(10):
            if not self.is_running:
              return
            self.progress_signal.emit((i+1)*10)
            QThread.msleep(50)
          search = Search()
          self.debug_callback(f"WorkerThread: Search: Вызов search_internet с параметрами: {self.parameters}")
          try:
              results = search.search_internet(self.parameters['query'])
              self.result_signal.emit(results if isinstance(results,str) else  f"Результаты поиска:\n {results}")
              self.debug_callback(f"WorkerThread: Search: Получен результат: {results}")
          except Exception as e:
              self.debug_callback(f"WorkerThread: Search: Ошибка поиска {e}")
              self.result_signal.emit(f"Ошибка поиска: {e}")
        else:
          self.result_signal.emit("Некорректный запрос поиска.")
          self.debug_callback(f"WorkerThread: Search: Некорректный запрос.")
      elif self.task == "calculator":
        if self.parameters:
            tasks = Tasks()
            self.debug_callback(f"WorkerThread: Calculator: Вызов create_calculator с параметрами: {self.parameters}")
            try:
              results = tasks.create_calculator(self.parameters)
              self.result_signal.emit(f"Результат: {results}")
              self.debug_callback(f"WorkerThread: Calculator: Получен результат: {results}")
            except Exception as e:
               self.debug_callback(f"WorkerThread: Calculator: Ошибка вычисления: {e}")
               self.result_signal.emit(f"Ошибка вычисления: {e}")
        else:
          self.result_signal.emit("Некорректный запрос калькулятора.")
          self.debug_callback(f"WorkerThread: Calculator: Некорректный запрос калькулятора.")
      else:
        self.result_signal.emit("Неизвестный запрос")
        self.debug_callback(f"WorkerThread: Неизвестный запрос: {self.task}, {self.parameters}")
      self.progress_signal.emit(100)

class InputWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QHBoxLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Введите запрос...")
        layout.addWidget(self.query_input)
        self.execute_button = QPushButton("Выполнить")
        self.execute_button.clicked.connect(self.main_window.execute_query)
        layout.addWidget(self.execute_button)
        self.setLayout(layout)

class OutputWidget(QTextEdit):
  def __init__(self):
        super().__init__()
        self.setReadOnly(True)

class DebugWidget(QTextEdit):
  def __init__(self):
        super().__init__()
        self.setReadOnly(True)

class FeedbackButton(QPushButton):
    def __init__(self, main_window):
        super().__init__("Оценить результат")
        self.main_window = main_window
        self.clicked.connect(self.main_window.give_feedback)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самообучающийся Персональный Ассистент (СПА)")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        # Input
        self.input_widget = InputWidget(self)
        self.layout.addWidget(self.input_widget)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.result_output = OutputWidget()
        self.layout.addWidget(self.result_output)
        
        self.debug_output = DebugWidget()
        self.layout.addWidget(self.debug_output)
        
        self.worker_thread = None

        # Инициализация модулей
        self.memory = Memory()
        self.parser = Parser()
        self.search = Search()
        self.engine = Engine()
        self.tasks = Tasks()
        self.self_analysis = SelfAnalysis()
        self.self_analysis.set_memory(self.memory)
        self.files = Files()
        
        self.feedback_button = FeedbackButton(self)
        self.layout.addWidget(self.feedback_button)
        self.last_query = None
        self.load_state()
        
    def closeEvent(self, event):
        self.save_state()
        self.memory.db.close()
        event.accept()

    def execute_query(self):
        self.progress_bar.setValue(0)
        query = self.input_widget.query_input.text()
        self.last_query = query
        self.result_output.append(f"Запрос: {query}\n")
        self._debug(f"GUI: Запрос: {query}")
        query_type, words = self.parser.parse_query(query)
        self._debug(f"GUI: Парсер: {query_type}, {words}")
        
        if self.worker_thread and self.worker_thread.isRunning():
          self.worker_thread.stop()
          self.worker_thread.wait()
          self.progress_bar.setValue(0)
        
        if query_type == "поиск":
            self.start_worker_thread("search", {'query':" ".join(words[1:])}, self._debug)
        elif query_type == "калькулятор":
            self.start_worker_thread("calculator", " ".join(words[1:]), self._debug)
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
            self._debug(f"GUI: Неизвестный запрос.")
        self.self_analysis.record_interaction(query, "OK")
        self.memory.add_past_action(str(datetime.datetime.now()), query, "OK")
    
    def start_worker_thread(self, task, parameters = None, debug_callback = None):
        self.progress_bar.setValue(0)
        self.worker_thread = WorkerThread(task, parameters, debug_callback)
        self.worker_thread.progress_signal.connect(self.update_progress_bar)
        self.worker_thread.result_signal.connect(self.handle_worker_result)
        self.worker_thread.start()
      
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)
      
    def handle_worker_result(self, results):
      self.result_output.append(f"{results}\n")
      self._debug(f"GUI: Результат: {results}")

    def handle_search(self, words):
        search_query = " ".join(words[1:])
        self._debug(f"GUI: handle_search: Запрос {search_query}")
        try:
            results = self.search.search_internet(search_query)
            if isinstance(results, str):
                self.result_output.append(results + "\n")
                self._debug(f"GUI: handle_search: Результат поиска: {results}")
            else:
                self.result_output.append("Результаты поиска:\n")
                for result in results:
                    self.result_output.append(f"{result['title']}: {result['url']}\n")
                self._debug(f"GUI: handle_search: Результат поиска: {results}")
        except Exception as e:
          self._debug(f"GUI: handle_search: Ошибка поиска: {e}")

    def extract_text_from_url(self, url):
        self._debug(f"GUI: extract_text_from_url: Запрос {url}")
        try:
            text = self.search.extract_text_from_url(url)
            if isinstance(text, str):
                self.result_output.append(f"Текст со страницы {url}:\n{text[:500]}...\n")
                self._debug(f"GUI: extract_text_from_url: Текст со страницы {url}:\n{text[:500]}...\n")
            else:
                self.result_output.append(f"Ошибка при извлечении текста: {text}\n")
                self._debug(f"GUI: extract_text_from_url: Ошибка при извлечении текста: {text}")
        except Exception as e:
          self._debug(f"GUI: extract_text_from_url: Ошибка: {e}")


    def handle_calculator(self, words):
        expression = " ".join(words[1:])
        self._debug(f"GUI: handle_calculator: Запрос {expression}")
        try:
           result = self.tasks.create_calculator(expression)
           self.result_output.append(f"Результат: {result}\n")
           self._debug(f"GUI: handle_calculator: Результат калькулятора: {result}")
        except Exception as e:
            self._debug(f"GUI: handle_calculator: Ошибка вычисления: {e}")


    def handle_code(self, words):
        prompt = " ".join(words[1:])
        self._debug(f"GUI: handle_code: Запрос: {prompt}")
        generated_code = self.engine.generate_text(prompt)
        self.result_output.append(f"Сгенерированный код:\n{generated_code}\n")
        self._debug(f"GUI: handle_code: Сгенерированный код:\n{generated_code}\n")

    def handle_learning(self, words):
        search_query = " ".join(words[1:]) + " обучение python"
        self._debug(f"GUI: handle_learning: Запрос {search_query}")
        try:
            results = self.search.search_internet(search_query)
            if isinstance(results, str):
                self.result_output.append(results + "\n")
                self._debug(f"GUI: handle_learning: Результаты поиска по обучению Python: {results}\n")
            else:
                self.result_output.append("Результаты поиска по обучению Python:\n")
                for result in results:
                    self.result_output.append(f"{result['title']}: {result['url']}\n")
                self._debug(f"GUI: handle_learning: Результаты поиска по обучению Python: {results}\n")
        except Exception as e:
          self._debug(f"GUI: handle_learning: Ошибка: {e}")

    def handle_interface(self, words):
        if "кнопку" in words:
            self.create_button()
        elif "поле ввода" in words:
            self.create_input_field()
        elif "текстовое поле" in words:
            self.create_text_field()
        elif "выпадающий список" in words:
            self.create_combo_box()
        elif "изменить текст кнопки" in words:
            self.change_button_text(words)
        else:
            self.result_output.append("Неизвестный запрос интерфейса.\n")
            self._debug(f"GUI: handle_interface: Неизвестный запрос интерфейса: {words}\n")

    def create_button(self):
        button = QPushButton("Новая кнопка")
        button.clicked.connect(lambda: self.result_output.append("Кнопка нажата!\n"))
        self.layout.addWidget(button)
        self.result_output.append("Кнопка создана.\n")
        self._debug(f"GUI: create_button: Создана кнопка.\n")

    def create_input_field(self):
        input_field = QLineEdit()
        input_field.setPlaceholderText("Введите текст...")
        self.layout.addWidget(input_field)
        self.result_output.append("Поле ввода создано.\n")
        self._debug(f"GUI: create_input_field: Создано поле ввода.\n")

    def create_text_field(self):
        text_field = QTextEdit()
        text_field.setReadOnly(True)
        self.layout.addWidget(text_field)
        self.result_output.append("Текстовое поле создано.\n")
        self._debug(f"GUI: create_text_field: Создано текстовое поле.\n")

    def create_combo_box(self):
        combo_box = QComboBox()
        combo_box.addItems(["Пункт 1", "Пункт 2", "Пункт 3"])
        self.layout.addWidget(combo_box)
        self.result_output.append("Выпадающий список создан.\n")
        self._debug(f"GUI: create_combo_box: Создан выпадающий список.\n")

    def change_button_text(self, words):
        if len(words) < 5:
            self.result_output.append("Недостаточно аргументов для изменения текста кнопки.\n")
            self._debug(f"GUI: change_button_text: Недостаточно аргументов для изменения текста кнопки: {words}\n")
            return
        try:
            button_index = int(words[3])
            new_text = " ".join(words[4:])
            button = self.layout.itemAt(button_index).widget()
            if isinstance(button, QPushButton):
                button.setText(new_text)
                self.result_output.append(f"Текст кнопки {button_index} изменен на '{new_text}'.\n")
                self._debug(f"GUI: change_button_text: Текст кнопки {button_index} изменен на '{new_text}'.\n")
            else:
                self.result_output.append(f"Элемент {button_index} не является кнопкой.\n")
                self._debug(f"GUI: change_button_text: Элемент {button_index} не является кнопкой.\n")
        except ValueError:
            self.result_output.append("Некорректный индекс кнопки.\n")
            self._debug(f"GUI: change_button_text: Некорректный индекс кнопки.\n")
        except Exception as e:
            self.result_output.append(f"Ошибка при изменении текста кнопки: {e}\n")
            self._debug(f"GUI: change_button_text: Ошибка при изменении текста кнопки: {e}\n")

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
            self._debug(f"GUI: load_file: Текст из PDF {file_path}:\n{text[:500]}...\n")

    def save_file(self):
        text_to_save = self.result_output.toPlainText()
        result = self.files.save_file(text_to_save)
        if result:
            self.result_output.append(result + "\n")
            self._debug(f"GUI: save_file: Файл сохранен в {result}.\n")

    def handle_memory(self, words):
        if "сохранить" in words:
            memory_data = self.memory.save_memory()
            self.result_output.append(f"Память сохранена:\n{memory_data}\n")
            self._debug(f"GUI: handle_memory: Память сохранена:\n{memory_data}\n")
        elif "загрузить" in words:
            # Здесь будет логика загрузки памяти
            self.result_output.append("Загрузка памяти пока не реализована.\n")
            self._debug(f"GUI: handle_memory: Загрузка памяти пока не реализована.\n")
        elif "поиск" in words:
            search_query = " ".join(words[1:])
            results = self.memory.search_memory(search_query)
            self.result_output.append(f"Результаты поиска в памяти:\n{results}\n")
            self._debug(f"GUI: handle_memory: Результаты поиска в памяти:\n{results}\n")
        elif "анализ" in words:
            analysis = self.memory.analyze_memory()
            self.result_output.append(f"Анализ памяти:\n{analysis}\n")
            self._debug(f"GUI: handle_memory: Анализ памяти:\n{analysis}\n")
        elif "план" in words:
            plan = self.memory.plan_actions()
            self.result_output.append(f"План действий:\n{plan}\n")
            self._debug(f"GUI: handle_memory: План действий:\n{plan}\n")
        elif "обновить" in words:
            key = words[2]
            value = " ".join(words[3:])
            self.memory.update_memory(key, value)
            self.result_output.append(f"Память обновлена: {key} = {value}\n")
            self._debug(f"GUI: handle_memory: Память обновлена: {key} = {value}\n")
        elif "получить" in words:
            key = " ".join(words[2:])
            value = self.memory.get_memory(key)
            self.result_output.append(f"Значение из памяти: {key} = {value}\n")
            self._debug(f"GUI: handle_memory: Значение из памяти: {key} = {value}\n")
        elif "очистить" in words:
            self.memory.db.clear()
            self.memory._load_initial_data()
            self.result_output.append(f"Память очищена.\n")
            self._debug(f"GUI: handle_memory: Память очищена.\n")
        else:
            self.result_output.append("Неизвестный запрос памяти.\n")
            self._debug(f"GUI: handle_memory: Неизвестный запрос памяти.\n")
    
    def give_feedback(self):
      feedback =  QMessageBox.question(self, "Оцените результат", "Как вы оцениваете результат?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
      if feedback == QMessageBox.StandardButton.Yes:
        self.self_analysis.get_feedback("Положительная оценка: " + self.last_query)
        self.result_output.append("Оценка положительная\n")
        self._debug(f"GUI: give_feedback: Получена положительная оценка: {self.last_query}\n")
      elif feedback == QMessageBox.StandardButton.No:
          self.self_analysis.get_feedback("Отрицательная оценка: " + self.last_query)
          self.result_output.append("Оценка отрицательная\n")
          self._debug(f"GUI: give_feedback: Получена отрицательная оценка: {self.last_query}\n")

    def save_state(self):
      self._debug(f"GUI: save_state: Сохраняю состояние")
      self.handle_memory(["память", "сохранить"])
      self._debug(f"GUI: save_state: Состояние сохранено")
      
    def load_state(self):
      self._debug(f"GUI: load_state: Загружаю состояние")
      self.memory._load_initial_data()
      self._debug(f"GUI: load_state: Состояние загружено")

    def _debug(self, message):
        self.debug_output.append(f"{message}\n")