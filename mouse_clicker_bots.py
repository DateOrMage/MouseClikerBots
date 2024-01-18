import sys

import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtSql import QSqlTableModel
from PySide6.QtCore import Signal, Slot, QRunnable, QThreadPool, QObject, QByteArray, QThread

from ui_interface import Ui_MainWindow, MatplotlibWidget

from pandas import DataFrame
from numpy import ndarray
from sklearn.manifold import TSNE
import traceback

from load_file import LoadFile
from classification_bots import ClassificationBots
from support_plot import get_x_y_cooor_and_label
from clusterization import Clusterization


class WorkerSignals(QObject):
    result = Signal(object)
    finished = Signal()
    error = Signal(str)


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
            self.signals.error.emit((traceback.format_exc()))
        else:
            self.signals.result.emit(res_func)
        finally:
            self.signals.finished.emit()


class MouseClicker(QMainWindow):
    def __init__(self):
        super(MouseClicker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.set_init_ui_settings()

        self.threadpool = QThreadPool()

        self.ui.but_load_excel.clicked.connect(self.start_thread_load_excel)
        self.ui.but_analyze.clicked.connect(self.start_thread_analyze_data)
        self.ui.but_plot_trajectories.clicked.connect(self.start_thread_plot_track)
        self.ui.but_clusterize.clicked.connect(self.start_thread_clusterize)
        self.ui.but_plot_tsne.clicked.connect(self.start_thread_plot_tsne)
        self.ui.but_save_tab_init.clicked.connect(self.start_thread_save_init_df)
        self.ui.but_save_tab_users.clicked.connect(self.start_thread_save_users_df)
        self.ui.but_filtred_users.clicked.connect(self.start_thread_sessions_by_users)
        self.ui.but_plot_trajectories_end.clicked.connect(self.start_thread_plot_track_end)

        self.data: DataFrame | None = None
        self.data_users: DataFrame | None = None
        self.tsne_data: ndarray | None = None

    def error_perform(self, traceback_info):
        self.ui.label_load.setText(traceback_info)
        self.ui.tabWidget.setCurrentIndex(0)

    # def set_init_ui_settings(self):
    #     pm_icon = QPixmap()
    #     pm_icon.loadFromData(QByteArray(ICON_BYTES_STR))
    #     self.setWindowIcon(QIcon(pm_icon))

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
            self.ui.label_load.setText("Подождите, идет загрузка...")
            self.ui.progress_analyze.setMaximum(0)
            self.ui.progress_analyze.setValue(-1)

            lf = LoadFile(file_path)
            thread_load = Worker(lf.execute)
            thread_load.signals.result.connect(self.result_load)
            thread_load.signals.error.connect(self.error_perform)
            thread_load.signals.finished.connect(self.finished_load)

            self.threadpool.start(thread_load)

    def result_analyze(self, res):
        self.data = res
        self.ui.label_load.setText("Данные успешно проанализированы, можно строить графики траекторий или"
                                   " кластеризовать данные.")
        self.ui.but_analyze.setEnabled(False)
        self.ui.but_clusterize.setEnabled(True)
        self.ui.label_table_init.setVisible(True)
        self.ui.but_plot_trajectories.setVisible(True)
        self.ui.but_save_tab_init.setVisible(True)

        self.ui.tableWidget_init.set_dataframe(self.data.drop(['x_y_unix'], axis=1).reset_index())

        self.ui.tabWidget.setCurrentIndex(1)

    def finished_analyze(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)

    def start_thread_analyze_data(self):
        self.ui.label_load.setText("Подождите, анализируются данные...")
        self.ui.progress_analyze.setMaximum(0)
        self.ui.progress_analyze.setValue(-1)

        cb = ClassificationBots()
        thread_analyze = Worker(cb.execute, self.data)
        thread_analyze.signals.result.connect(self.result_analyze)
        thread_analyze.signals.error.connect(self.error_perform)
        thread_analyze.signals.finished.connect(self.finished_analyze)

        self.threadpool.start(thread_analyze)

    # plot trajectories
    def plot_track(self, table_widget: str):
        self.ui.matplotlib_traj_widget.reset_widget()
        if table_widget == 'init':
            selected_indices_track = self.ui.tableWidget_init.get_values_of_selected_items()
        elif table_widget == 'session':
            selected_indices_track = self.ui.tableWidget_sessions.get_values_of_selected_items()
        else:
            selected_indices_track = []
        selected_indices_track = [int(id_session) for id_session in selected_indices_track]
        self.ui.matplotlib_traj_widget.canvas.axes.set_xlabel('X Coordinate')
        self.ui.matplotlib_traj_widget.canvas.axes.set_ylabel('Y Coordinate')
        self.ui.matplotlib_traj_widget.canvas.axes.set_title(f'Bot Trajectory')
        for value in selected_indices_track:
            x_coords, y_coords, label = get_x_y_cooor_and_label(self.data, self.ui.tableWidget_init.checkbox_list[0],
                                                                value)
            self.ui.matplotlib_traj_widget.canvas.axes.plot(x_coords, y_coords, marker='o', linestyle='-', label=label)
        self.ui.matplotlib_traj_widget.canvas.axes.legend()

    def result_plot_track(self):
        self.ui.matplotlib_traj_widget.canvas.draw()
        self.ui.tabWidget.setCurrentIndex(2)

    def finished_plot_track(self):
        pass

    def start_thread_plot_track(self):
        thread_plot_track = Worker(self.plot_track, 'init')
        thread_plot_track.signals.result.connect(self.result_plot_track)
        thread_plot_track.signals.error.connect(self.error_perform)
        thread_plot_track.signals.finished.connect(self.finished_plot_track)

        self.threadpool.start(thread_plot_track)

    def result_clusterize(self, res):
        self.data = res[0]
        self.data_users = res[1]
        self.tsne_data = res[2]
        self.ui.label_load.setText("Кластеризация прошла успешно, можно строить графики траекторий, кластеризации или"
                                   " рассмотреть сессии пользователя.")
        self.ui.but_clusterize.setEnabled(False)
        self.ui.label_user.setVisible(True)
        self.ui.but_plot_tsne.setVisible(True)
        self.ui.but_filtred_users.setVisible(True)
        self.ui.but_save_tab_users.setVisible(True)

        self.ui.tableWidget_users.set_dataframe(self.data_users.reset_index())

        self.ui.tabWidget.setCurrentIndex(3)

    def finished_clusterize(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)

    def start_thread_clusterize(self):
        self.ui.label_load.setText("Подождите, идет кластеризация данных...")
        self.ui.progress_analyze.setMaximum(0)
        self.ui.progress_analyze.setValue(-1)

        cluster = Clusterization()
        thread_cluster = Worker(cluster.execute, self.data)
        thread_cluster.signals.result.connect(self.result_clusterize)
        thread_cluster.signals.error.connect(self.error_perform)
        thread_cluster.signals.finished.connect(self.finished_clusterize)

        self.threadpool.start(thread_cluster)

    def plot_tsne(self):
        self.ui.matplotlib_tsne_widget.reset_widget()
        self.ui.matplotlib_tsne_widget.canvas.axes.set_xlabel('t-SNE Dimension 1')
        self.ui.matplotlib_tsne_widget.canvas.axes.set_ylabel('t-SNE Dimension 2')
        self.ui.matplotlib_tsne_widget.canvas.axes.set_title(f't-SNE Visualization with Clusters')

        tsne = TSNE(n_components=2, random_state=42)
        tsne_data = tsne.fit_transform(self.tsne_data)
        n_clusters = self.data_users['User_cluster'].nunique()

        for i in range(n_clusters):
            self.ui.matplotlib_tsne_widget.canvas.axes.scatter(tsne_data[self.data_users['User_cluster'] == i, 0],
                                                               tsne_data[self.data_users['User_cluster'] == i, 1],
                                                               label={0: "Не бот (0)", 1: "Бот (1)",
                                                                      2: "Бот (2)", 3: "Бот (3)", 4: "Бот (4)",
                                                                      5: "Бот (5)"}[i],
                                                               #s=5
                                                               )
        self.ui.matplotlib_tsne_widget.canvas.axes.legend()

    def result_plot_tsne(self):
        self.ui.matplotlib_tsne_widget.canvas.draw()
        self.ui.tabWidget.setCurrentIndex(4)

    def finished_plot_tsne(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)

    def start_thread_plot_tsne(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.progress_analyze.setMaximum(0)
        self.ui.progress_analyze.setValue(-1)

        thread_plot_tsne = Worker(self.plot_tsne)
        thread_plot_tsne.signals.result.connect(self.result_plot_tsne)
        thread_plot_tsne.signals.error.connect(self.error_perform)
        thread_plot_tsne.signals.finished.connect(self.finished_plot_tsne)

        self.threadpool.start(thread_plot_tsne)

    def save_df(self, file_name):
        self.data.to_excel(file_name)
        return file_name

    def result_save_init_df(self, file_name):
        self.ui.label_load.setText(f'Данные по ботам сохранены в: {file_name}')

    def finished_save_init_df(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)

    def start_thread_save_init_df(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить датафрейм", "",
                                                   "Excel Files (*.xlsx);;All Files (*)")

        if file_name:
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.label_load.setText("Подождите, идет сохранение...")
            self.ui.progress_analyze.setMaximum(0)
            self.ui.progress_analyze.setValue(-1)

            thread_save = Worker(self.save_df, file_name)
            thread_save.signals.result.connect(self.result_save_init_df)
            thread_save.signals.error.connect(self.error_perform)
            thread_save.signals.finished.connect(self.finished_save_init_df)

            self.threadpool.start(thread_save)

    def save_users_df(self, file_name: str):
        self.data_users.to_excel(file_name)
        return file_name

    def result_save_users_df(self, file_name: str):
        self.ui.label_load.setText(f'Данные по пользователям сохранены в: {file_name}')

    def finished_save_users_df(self):
        self.ui.progress_analyze.setMaximum(1)
        self.ui.progress_analyze.setValue(1)

    def start_thread_save_users_df(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить датафрейм", "",
                                                   "Excel Files (*.xlsx);;All Files (*)")

        if file_name:
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.label_load.setText("Подождите, идет сохранение...")
            self.ui.progress_analyze.setMaximum(0)
            self.ui.progress_analyze.setValue(-1)

            thread_save = Worker(self.save_users_df, file_name)
            thread_save.signals.result.connect(self.result_save_users_df)
            thread_save.signals.error.connect(self.error_perform)
            thread_save.signals.finished.connect(self.finished_save_users_df)

            self.threadpool.start(thread_save)

    # session by users
    def sessions_by_users(self):

        self.selected_indices_users = self.ui.tableWidget_users.get_values_of_selected_items()
        print(self.selected_indices_users)
        df_users_list = []
        for user in self.selected_indices_users:
            df_users_list.append(self.data[self.data['ACCOUNT_ID'] == user])
        self.df_session_by_users = pd.concat(df_users_list, axis=0)
        # self.ui.tableWidget_sessions.set_dataframe(df_session_by_users.drop(['x_y_unix'], axis=1).reset_index())

    def result_sessions_by_users(self):
        self.ui.tableWidget_sessions.set_dataframe(self.df_session_by_users.drop(['x_y_unix'], axis=1).reset_index())
        self.ui.label_sessions.setVisible(True)
        self.ui.but_plot_trajectories_end.setVisible(True)
        self.ui.but_plot_trajectories_end.setEnabled(True)
        self.ui.tabWidget.setCurrentIndex(5)

    def finished_sessions_by_users(self):
        pass

    def start_thread_sessions_by_users(self):
        thread_sessions_by_users = Worker(self.sessions_by_users)
        thread_sessions_by_users.signals.result.connect(self.result_sessions_by_users)
        thread_sessions_by_users.signals.error.connect(self.error_perform)
        thread_sessions_by_users.signals.finished.connect(self.finished_sessions_by_users)

        self.threadpool.start(thread_sessions_by_users)

    def start_thread_plot_track_end(self):
        thread_plot_track_end = Worker(self.plot_track, 'session')
        thread_plot_track_end.signals.result.connect(self.result_plot_track)
        thread_plot_track_end.signals.error.connect(self.error_perform)
        thread_plot_track_end.signals.finished.connect(self.finished_plot_track)

        self.threadpool.start(thread_plot_track_end)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseClicker()
    window.show()

    sys.exit(app.exec())
