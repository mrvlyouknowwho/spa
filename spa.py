# spa.py
import sys
from PyQt6.QtWidgets import QApplication
from modules.gui import MainWindow
from modules.self_analysis import SelfAnalysis

if __name__ == "__main__":
    print("spa.py: Запуск приложения")
    app = QApplication(sys.argv)
    print("spa.py: QApplication создан")
    window = MainWindow()
    if hasattr(window, 'memory'):
        self_analysis = SelfAnalysis()
        self_analysis.set_memory(window.memory)
        print("spa.py: SelfAnalysis установлен")
    else:
        print("spa.py: Ошибка: window.memory не инициализирован")
    window.show()
    print("spa.py: Главное окно показано")
    sys.exit(app.exec())