import sys
from PyQt6.QtWidgets import QApplication
from modules.gui import MainWindow
from modules.self_analysis import SelfAnalysis

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    self_analysis = SelfAnalysis()
    self_analysis.set_memory(window.memory)
    window.show()
    sys.exit(app.exec())