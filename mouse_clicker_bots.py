import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtSql import QSqlTableModel
from PySide6.QtCore import Signal, Slot, QRunnable, QThreadPool, QObject, QByteArray

from ui_interface import Ui_MainWindow

from pandas import DataFrame

from load_file import LoadFile


class MouseClicker(QMainWindow):
    def __init__(self):
        super(MouseClicker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()

        self.ui.but_load_excel.clicked.connect(self.load_excel)

        self.data: DataFrame | None = None

    def load_excel(self):
        # options = QFileDialog.Options()
        self.ui.but_analyze.setEnabled(False)
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл эксель", "",
                                                   "Excel Files (*.xlsx);;All Files (*)")  # options=options)
        if file_path:
            lf = LoadFile(file_path)
            self.data, text_print, flag_load = lf.execute()
            self.ui.label_load.setText(text_print)
            if flag_load:
                self.ui.but_analyze.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseClicker()
    window.show()

    sys.exit(app.exec())
