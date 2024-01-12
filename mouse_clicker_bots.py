import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtSql import QSqlTableModel
from PySide6.QtCore import Signal, Slot, QRunnable, QThreadPool, QObject, QByteArray, QThread

from ui_interface import Ui_MainWindow

from pandas import DataFrame

from load_file import LoadFile
from classification_bots import ClassificationBots
# from s_table_widet import STableWidet


class WorkerSignals(QObject):
    result = Signal(object)
    finished = Signal()


class Worker(QRunnable):
    def __init__(self, my_func, *args):
        super(Worker, self).__init__()
        self.my_func = my_func
        self.args = args
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            res_func = self.my_func(*self.args)
        except:
            pass
        else:
            self.signals.result.emit(res_func)
        finally:
            self.signals.finished.emit()


class MouseClicker(QMainWindow):
    def __init__(self):
        super(MouseClicker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()

        self.ui.but_load_excel.clicked.connect(self.start_thread_load_excel)
        self.ui.but_analyze.clicked.connect(self.start_thread_analyze_data)

        self.data: DataFrame | None = None

    def result_load(self, res):
        self.data = res[0]  # data
        self.ui.label_load.setText(res[1])  # text_print
        if res[2]:  # flag_load:
            self.ui.but_analyze.setEnabled(True)

    def finished_load(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)

    def start_thread_load_excel(self):
        self.ui.but_analyze.setEnabled(False)
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл эксель", "",
                                                   "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            # PROGRESS BAR
            self.ui.label_load.setText("Подождите, идет загрузка")
            self.ui.progress_analyze.setMaximum(0)
            self.ui.progress_analyze.setValue(-1)

            lf = LoadFile(file_path)
            # self.data, text_print, flag_load = lf.execute()

            thread_load = Worker(lf.execute)
            thread_load.signals.result.connect(self.result_load)
            thread_load.signals.finished.connect(self.finished_load)

            self.threadpool.start(thread_load)

    def result_analyze(self, res):
        self.data = res
        self.ui.label_load.setText("Данные успешно проанализированы, можно строить графики траекторий или"
                                   " кластеризовать данные")
        self.ui.but_analyze.setEnabled(False)
        self.ui.but_clusterize.setEnabled(True)
        self.ui.label_table_init.setVisible(True)
        self.ui.but_plot_trajectories.setVisible(True)
        self.ui.but_save_tab_init.setVisible(True)

        self.ui.tableWidget_init.set_dataframe(self.data.reset_index())
        # tableWidget_init = STableWidet(self.data, checkbox_list=['ID'], filter_only_if_return_pressed=True)
        # self.ui.verticalLayout_tab_init.addWidget(tableWidget_init)

        self.ui.tabWidget.setCurrentIndex(1)

    def finished_analyze(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)
        # print(self.data)

    def start_thread_analyze_data(self):
        self.ui.label_load.setText("Подождите, анализируются данные")
        self.ui.progress_analyze.setMaximum(0)
        self.ui.progress_analyze.setValue(-1)

        cb = ClassificationBots()
        thread_analyze = Worker(cb.execute, self.data)
        thread_analyze.signals.result.connect(self.result_analyze)
        thread_analyze.signals.finished.connect(self.finished_analyze)

        self.threadpool.start(thread_analyze)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseClicker()
    window.show()

    sys.exit(app.exec())
