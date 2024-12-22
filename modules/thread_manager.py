# modules/thread_manager.py
from PyQt6.QtCore import QThread, pyqtSignal
from modules.search import Search
from modules.tasks import Tasks
import traceback

class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, task, parameters=None, debug_callback=None):
        super().__init__()
        self.task = task
        self.parameters = parameters
        self.is_running = True
        self.debug_callback = debug_callback
    
    def stop(self):
       self.is_running = False

    def run(self):
        self.debug_callback(f"WorkerThread: run: Task: {self.task}, Parameters: {self.parameters}", 'thread_manager')
        try:
            if self.task == "search":
                if self.parameters and 'query' in self.parameters:
                    for i in range(10):
                        if not self.is_running:
                            return
                        self.progress_signal.emit((i+1)*10)
                        QThread.msleep(50)
                    search = Search()
                    self.debug_callback(f"WorkerThread: Search: Вызов search_internet с параметрами: {self.parameters}", 'thread_manager')
                    try:
                        results, error = search.search_internet(self.parameters['query'])
                        if error:
                            self.error_signal.emit(f"Ошибка поиска: {results}")
                            self.debug_callback(f"WorkerThread: Search: Ошибка поиска {results}", 'thread_manager')
                        else:
                            self.result_signal.emit(f"Результаты поиска:\n {results}")
                            self.debug_callback(f"WorkerThread: Search: Получен результат: {results}", 'thread_manager')
                    except Exception as e:
                        self.debug_callback(f"WorkerThread: Search: Ошибка поиска {e}", 'thread_manager')
                        self.error_signal.emit(f"Ошибка поиска: {e}")
                else:
                    self.result_signal.emit("Некорректный запрос поиска.")
                    self.debug_callback(f"WorkerThread: Search: Некорректный запрос.", 'thread_manager')
            elif self.task == "calculator":
                if self.parameters:
                    tasks = Tasks()
                    self.debug_callback(f"WorkerThread: Calculator: Вызов create_calculator с параметрами: {self.parameters}", 'thread_manager')
                    try:
                        results, error = tasks.create_calculator(self.parameters)
                        if error:
                           self.error_signal.emit(f"Ошибка вычисления: {results}")
                           self.debug_callback(f"WorkerThread: Calculator: Ошибка вычисления: {results}", 'thread_manager')
                        else:
                          self.result_signal.emit(f"Результат: {results}")
                          self.debug_callback(f"WorkerThread: Calculator: Получен результат: {results}", 'thread_manager')
                    except Exception as e:
                       self.debug_callback(f"WorkerThread: Calculator: Ошибка вычисления: {e}", 'thread_manager')
                       self.error_signal.emit(f"Ошибка вычисления: {e}")
                else:
                    self.result_signal.emit("Некорректный запрос калькулятора.")
                    self.debug_callback(f"WorkerThread: Calculator: Некорректный запрос калькулятора.", 'thread_manager')
            else:
                self.result_signal.emit("Неизвестный запрос")
                self.debug_callback(f"WorkerThread: Неизвестный запрос: {self.task}, {self.parameters}", 'thread_manager')
            self.progress_signal.emit(100)
        except Exception as e:
            self.debug_callback(f"WorkerThread: Ошибка в потоке: {e}, {traceback.format_exc()}", 'thread_manager')
            self.error_signal.emit(f"Ошибка в потоке: {e}")
      
class ThreadManager:
    def __init__(self, debug_callback):
        print("ThreadManager: Инициализация")
        self.debug_callback = debug_callback
        self.worker_thread = None

    def start_worker_thread(self, task, parameters = None, progress_callback = None, result_callback = None, error_callback = None):
        if self.worker_thread and self.worker_thread.isRunning():
          self.worker_thread.stop()
          self.worker_thread.wait()
        
        self.worker_thread = WorkerThread(task, parameters, self.debug_callback)
        if progress_callback:
            self.worker_thread.progress_signal.connect(progress_callback)
        if result_callback:
            self.worker_thread.result_signal.connect(result_callback)
        if error_callback:
            self.worker_thread.error_signal.connect(error_callback)
        self.worker_thread.start()