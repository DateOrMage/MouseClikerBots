import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSql import QSqlTableModel

from ui_interface import Ui_MainWindow


class MouseClicker(QMainWindow):
    def __init__(self):
        super(MouseClicker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseClicker()
    window.show()

    sys.exit(app.exec())
