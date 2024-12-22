# modules/gui.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QComboBox, QLabel, QProgressBar, QHBoxLayout,
                             QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QClipboard
from modules.parser import Parser
from modules.search import Search
from modules.engine import Engine
from modules.tasks import Tasks
from modules.self_analysis import SelfAnalysis
from modules.files import Files
from modules.memory import Memory
from modules.app_manager import AppManager
from modules.thread_manager import ThreadManager
from config import Config
from logger import Logger

import datetime

class InputWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QHBoxLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Введите запрос...")
        self.query_input.returnPressed.connect(self.main_window.execute_query)
        layout.addWidget(self.query_input)
        self.execute_button = QPushButton("Выполнить")
        self.execute_button.clicked.connect(self.main_window.execute_query)
        layout.addWidget(self.execute_button)
        self.setLayout(layout)

class OutputWidget(QTextEdit):
  def __init__(self):
        super().__init__()
        self.setReadOnly(True)

class FeedbackButton(QPushButton):
    def __init__(self, main_window):
        print("FeedbackButton: Инициализация - Начало")
        super().__init__("Оценить результат")
        self.main_window = main_window
        self.clicked.connect(self.main_window.give_feedback)
        print("FeedbackButton: Инициализация - Конец")
        
class MainWindow(QMainWindow):
    def __init__(self):
        print("MainWindow: Инициализация - Начало")
        super().__init__()
        self.setWindowTitle("Самообучающийся Персональный Ассистент (СПА)")
        self.setGeometry(100, 100, 800, 600)
        print("MainWindow: Настройка окна")

        self.config = Config()
        print("MainWindow: Инициализирован Config")
        self.logger = Logger(self.config)
        print("MainWindow: Инициализирован Logger")
        try:
            print("MainWindow: Инициализация Memory - Начало")
            self.memory = Memory()
            print("MainWindow: Инициализирован Memory - Конец")
            print("MainWindow: Инициализация ThreadManager - Начало")
            self.thread_manager = ThreadManager(self._debug)
            print("MainWindow: Инициализирован ThreadManager - Конец")
            print("MainWindow: Инициализация AppManager - Начало")
            self.app_manager = AppManager(self.memory, self._debug)
            print("MainWindow: Инициализирован AppManager - Конец")

            self.central_widget = QWidget()
            print("MainWindow: Создание central_widget")
            self.setCentralWidget(self.central_widget)
            print("MainWindow: Установка central_widget")
            self.layout = QVBoxLayout(self.central_widget)
            print("MainWindow: Создание layout")
        
            # Input
            self.input_widget = InputWidget(self)
            print("MainWindow: Инициализирован InputWidget")
            self.layout.addWidget(self.input_widget)
            print("MainWindow: Добавлен InputWidget")
        
            self.progress_bar = QProgressBar()
            print("MainWindow: Инициализирован Progressbar")
            self.progress_bar.setValue(0)
            self.layout.addWidget(self.progress_bar)
            print("MainWindow: Добавлен Progressbar")

            self.result_output = OutputWidget()
            print("MainWindow: Инициализирован OutputWidget")
            self.layout.addWidget(self.result_output)
            print("MainWindow: Добавлен OutputWidget")
            
            try:
                
               self.feedback_button = FeedbackButton(self)
               print("MainWindow: Инициализирован FeedbackButton")
               self.layout.addWidget(self.feedback_button)
               print("MainWindow: Добавлен FeedbackButton")
            except Exception as e:
                print(f"MainWindow: Ошибка инициализации FeedbackButton: {e}")
                self.logger.error(f"MainWindow: Ошибка инициализации FeedbackButton: {e}")
            
            self.last_query = None
            self.load_state()
            print("MainWindow: Инициализация - Конец")
            self.show()
            print("MainWindow: Показано окно")
            print("MainWindow: Приложение запущено")
        except Exception as e:
            print(f"MainWindow: Ошибка инициализации: {e}")
            self.logger.error(f"MainWindow: Ошибка инициализации: {e}")
            QMessageBox.critical(self, "Ошибка инициализации", f"Произошла ошибка при инициализации приложения: {e}")
            self.close()
            
    def closeEvent(self, event):
        self.save_state()
        if hasattr(self, 'memory') and self.memory.db:
             self.memory.db.close()
        event.accept()

    def execute_query(self):
        self._debug(f"GUI: execute_query: Запрос начат", 'gui')
        self.progress_bar.setValue(0)
        query = self.input_widget.query_input.text()
        self.last_query = query
        self.result_output.append(f"Запрос: {query}\n")
        self._debug(f"GUI: Запрос: {query}", 'gui')
        
        task, parameters = self.app_manager.execute_query(query)
        
        if task == "search" or task == "calculator":
          self.thread_manager.start_worker_thread(task, parameters, self.update_progress_bar, self.handle_worker_result)
        elif task == "code":
            result = self.app_manager.handle_code(parameters)
            self.result_output.append(f"Сгенерированный код:\n{result}\n")
        elif task == "learning":
             result = self.app_manager.handle_learning(parameters)
             if isinstance(result, str):
               self.result_output.append(result + "\n")
             else:
                self.result_output.append("Результаты поиска по обучению Python:\n")
                for item in result:
                    self.result_output.append(f"{item['title']}: {item['url']}\n")
        elif task == "interface":
            result = self.app_manager.handle_interface(parameters)
            if result == "create_button":
              self.create_button()
            elif result == "create_input_field":
              self.create_input_field()
            elif result == "create_text_field":
              self.create_text_field()
            elif result == "create_combo_box":
              self.create_combo_box()
            elif result == "change_button_text":
              self.change_button_text(parameters)
        elif task == "file":
          result = self.app_manager.handle_file(parameters)
          if result == "load_file":
            self.load_file()
          elif result == "save_file":
            self.save_file()
        elif task == "memory":
            result = self.app_manager.handle_memory(parameters)
            if result == "save_memory":
              self.save_memory()
            elif result == "load_memory":
              self.load_memory()
            elif result == "search_memory":
              self.search_memory(parameters)
            elif result == "analyze_memory":
              self.analyze_memory()
            elif result == "plan_memory":
              self.plan_memory()
            elif result == "update_memory":
                self.update_memory(parameters["key"], parameters["value"])
            elif result == "get_memory":
              self.get_memory(parameters)
            elif result == "clear_memory":
              self.clear_memory()
        else:
            self.result_output.append("Неизвестный запрос.\n")
            self._debug(f"GUI: Неизвестный запрос.", 'gui')
        self.app_manager.record_interaction(query, "OK")
      
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)
      
    def handle_worker_result(self, results):
      self.result_output.append(f"{results}\n")
      self._debug(f"GUI: Результат: {results}", 'gui')

    def create_button(self):
        button = QPushButton("Новая кнопка")
        button.clicked.connect(lambda: self.result_output.append("Кнопка нажата!\n"))
        self.layout.addWidget(button)
        self.result_output.append("Кнопка создана.\n")
        self._debug(f"GUI: create_button: Создана кнопка.\n", 'gui')

    def create_input_field(self):
        input_field = QLineEdit()
        input_field.setPlaceholderText("Введите текст...")
        self.layout.addWidget(input_field)
        self.result_output.append("Поле ввода создано.\n")
        self._debug(f"GUI: create_input_field: Создано поле ввода.\n", 'gui')

    def create_text_field(self):
        text_field = QTextEdit()
        text_field.setReadOnly(True)
        self.layout.addWidget(text_field)
        self.result_output.append("Текстовое поле создано.\n")
        self._debug(f"GUI: create_text_field: Создано текстовое поле.\n", 'gui')

    def create_combo_box(self):
        combo_box = QComboBox()
        combo_box.addItems(["Пункт 1", "Пункт 2", "Пункт 3"])
        self.layout.addWidget(combo_box)
        self.result_output.append("Выпадающий список создан.\n")
        self._debug(f"GUI: create_combo_box: Создан выпадающий список.\n", 'gui')

    def change_button_text(self, words):
        if len(words) < 5:
            self.result_output.append("Недостаточно аргументов для изменения текста кнопки.\n")
            self._debug(f"GUI: change_button_text: Недостаточно аргументов для изменения текста кнопки: {words}\n", 'gui')
            return
        try:
            button_index = int(words[3])
            new_text = " ".join(words[4:])
            button = self.layout.itemAt(button_index).widget()
            if isinstance(button, QPushButton):
                button.setText(new_text)
                self.result_output.append(f"Текст кнопки {button_index} изменен на '{new_text}'.\n")
                self._debug(f"GUI: change_button_text: Текст кнопки {button_index} изменен на '{new_text}'.\n", 'gui')
            else:
                self.result_output.append(f"Элемент {button_index} не является кнопкой.\n")
                self._debug(f"GUI: change_button_text: Элемент {button_index} не является кнопкой.\n", 'gui')
        except ValueError:
            self.result_output.append("Некорректный индекс кнопки.\n")
            self._debug(f"GUI: change_button_text: Некорректный индекс кнопки.\n", 'gui')
        except Exception as e:
            self.result_output.append(f"Ошибка при изменении текста кнопки: {e}\n")
            self._debug(f"GUI: change_button_text: Ошибка при изменении текста кнопки: {e}\n", 'gui')

    def load_file(self):
        file_path = self.app_manager.files.load_file()
        if file_path:
            text = self.app_manager.files.extract_text_from_pdf(file_path)
            self.result_output.append(f"Текст из PDF {file_path}:\n{text[:500]}...\n")
            self._debug(f"GUI: load_file: Текст из PDF {file_path}:\n{text[:500]}...\n", 'gui')

    def save_file(self):
        text_to_save = self.result_output.toPlainText()
        result = self.app_manager.files.save_file(text_to_save)
        if result:
            self.result_output.append(result + "\n")
            self._debug(f"GUI: save_file: Файл сохранен в {result}.\n", 'gui')

    def save_memory(self):
      try:
        memory_data = self.memory.save_memory()
        self.result_output.append(f"Память сохранена:\n{memory_data}\n")
        self._debug(f"GUI: handle_memory: Память сохранена:\n{memory_data}\n", 'gui')
      except Exception as e:
        self.result_output.append(f"Ошибка сохранения памяти: {e}\n")
        self._debug(f"GUI: handle_memory: Ошибка сохранения памяти: {e}\n", 'gui')

    def load_memory(self):
      try:
        self._debug(f"GUI: load_memory: Загрузка памяти начата", 'gui')
        self.memory._load_initial_data()
        self.result_output.append("Память загружена.\n")
        self._debug(f"GUI: handle_memory: Память загружена.\n", 'gui')
      except Exception as e:
        self.result_output.append(f"Ошибка загрузки памяти: {e}\n")
        self._debug(f"GUI: handle_memory: Ошибка загрузки памяти: {e}\n", 'gui')


    def search_memory(self, query):
      try:
        results = self.memory.search_memory(query)
        self.result_output.append(f"Результаты поиска в памяти:\n{results}\n")
        self._debug(f"GUI: handle_memory: Результаты поиска в памяти:\n{results}\n", 'gui')
      except Exception as e:
        self.result_output.append(f"Ошибка поиска в памяти: {e}\n")
        self._debug(f"GUI: handle_memory: Ошибка поиска в памяти: {e}\n", 'gui')

    def analyze_memory(self):
      try:
        analysis = self.memory.analyze_memory()
        self.result_output.append(f"Анализ памяти:\n{analysis}\n")
        self._debug(f"GUI: handle_memory: Анализ памяти:\n{analysis}\n", 'gui')
      except Exception as e:
         self.result_output.append(f"Ошибка анализа памяти: {e}\n")
         self._debug(f"GUI: handle_memory: Ошибка анализа памяти: {e}\n", 'gui')

    def plan_memory(self):
      try:
         plan = self.memory.plan_actions()
         self.result_output.append(f"План действий:\n{plan}\n")
         self._debug(f"GUI: handle_memory: План действий:\n{plan}\n", 'gui')
      except Exception as e:
          self.result_output.append(f"Ошибка планирования памяти: {e}\n")
          self._debug(f"GUI: handle_memory: Ошибка планирования памяти: {e}\n", 'gui')

    def update_memory(self, key, value):
      try:
        self.memory.update_memory(key, value)
        self.result_output.append(f"Память обновлена: {key} = {value}\n")
        self._debug(f"GUI: handle_memory: Память обновлена: {key} = {value}\n", 'gui')
      except Exception as e:
        self.result_output.append(f"Ошибка обновления памяти: {e}\n")
        self._debug(f"GUI: handle_memory: Ошибка обновления памяти: {e}\n", 'gui')

    def get_memory(self, key):
      try:
        value = self.memory.get_memory(key)
        self.result_output.append(f"Значение из памяти: {key} = {value}\n")
        self._debug(f"GUI: handle_memory: Значение из памяти: {key} = {value}\n", 'gui')
      except Exception as e:
        self.result_output.append(f"Ошибка получения значения из памяти: {e}\n")
        self._debug(f"GUI: handle_memory: Ошибка получения значения из памяти: {e}\n", 'gui')

    def clear_memory(self):
        try:
            self.memory.db.clear()
            self.memory._load_initial_data()
            self.result_output.append(f"Память очищена.\n")
            self._debug(f"GUI: handle_memory: Память очищена.\n", 'gui')
        except Exception as e:
          self.result_output.append(f"Ошибка очистки памяти: {e}\n")
          self._debug(f"GUI: handle_memory: Ошибка очистки памяти: {e}\n", 'gui')
    
    def give_feedback(self):
      feedback =  QMessageBox.question(self, "Оцените результат", "Как вы оцениваете результат?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
      if feedback == QMessageBox.StandardButton.Yes:
        self.app_manager.self_analysis.get_feedback("Положительная оценка: " + self.last_query)
        self.result_output.append("Оценка положительная\n")
        self._debug(f"GUI: give_feedback: Получена положительная оценка: {self.last_query}\n", 'gui')
      elif feedback == QMessageBox.StandardButton.No:
          self.app_manager.self_analysis.get_feedback("Отрицательная оценка: " + self.last_query)
          self.result_output.append("Оценка отрицательная\n")
          self._debug(f"GUI: give_feedback: Получена отрицательная оценка: {self.last_query}\n", 'gui')

    def save_state(self):
      self._debug(f"GUI: save_state: Сохраняю состояние", 'gui')
      try:
        self.app_manager.handle_memory(["память", "сохранить"])
        self._debug(f"GUI: save_state: Состояние сохранено", 'gui')
      except Exception as e:
        self._debug(f"GUI: save_state: Ошибка сохранения состояния: {e}", 'gui')
        self.result_output.append(f"Ошибка сохранения состояния: {e}\n")
      
    def load_state(self):
      self._debug(f"GUI: load_state: Загружаю состояние", 'gui')
      try:
        self.memory._load_initial_data()
        self._debug(f"GUI: load_state: Состояние загружено", 'gui')
      except Exception as e:
          self._debug(f"GUI: load_state: Ошибка загрузки состояния: {e}", 'gui')
          self.result_output.append(f"Ошибка загрузки состояния: {e}\n")

    def _debug(self, message, module=None):
      self.logger.debug(message)
      if hasattr(self, 'debug_output') and self.debug_output:
        self.debug_output.append(f"{message}\n")