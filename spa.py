import sys
from PyQt6.QtWidgets import QApplication
from modules.gui import MainWindow
from modules.self_learning import SelfLearning

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    self_learning = SelfLearning()
    self_learning.set_memory(window.memory)
    window.show()
    sys.exit(app.exec())