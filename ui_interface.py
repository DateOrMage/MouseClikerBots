import matplotlib.pyplot as plt

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QByteArray)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QProgressBar, QPushButton, QSizeGrip,
    QSizePolicy, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from s_table_widet import STableWidet

matplotlib.use('qtagg')
plt.ioff()


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None, figure=None):
        super(MatplotlibWidget, self).__init__(parent)

        # self.figure = Figure() if figure is None else figure
        self.canvas = PlotCanvas()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def reset_widget(self):
        self.canvas.axes.clear()



class PlotCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)


def create_tab_with_figure(figure=None):
    tab = QWidget()
    layout = QVBoxLayout()
    matplotlib_widget = MatplotlibWidget(figure=figure)
    layout.addWidget(matplotlib_widget)
    tab.setLayout(layout)
    return tab


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1360, 765) # 1200, 675
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # icon = QIcon()
        # icon.addFile(u"C:\\Users\\Пользователь\\Downloads\\free_icon_1.png", QSize(), QIcon.Normal)
        # MainWindow.setWindowIcon(icon)

        # central widget layout
        self.verticalLayout_central = QVBoxLayout(self.centralwidget)
        self.verticalLayout_central.setObjectName(u"verticalLayout_central")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)

        # tab load
        self.tab_load = QWidget()
        self.tab_load.setObjectName(u"tab_load")
        self.tab_load.setGeometry(QRect(100, 70, 771, 391))
        self.verticalLayout = QVBoxLayout(self.tab_load)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.but_load_excel = QPushButton(self.tab_load)
        self.but_load_excel.setObjectName(u"but_load_excel")

        self.verticalLayout.addWidget(self.but_load_excel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.but_analyze = QPushButton(self.tab_load)
        self.but_analyze.setObjectName(u"but_analyze")
        self.but_analyze.setEnabled(False)

        self.horizontalLayout.addWidget(self.but_analyze)

        self.but_clusterize = QPushButton(self.tab_load)
        self.but_clusterize.setObjectName(u"but_clusterize")
        self.but_clusterize.setEnabled(False)

        self.horizontalLayout.addWidget(self.but_clusterize)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.progress_analyze = QProgressBar(self.tab_load)
        self.progress_analyze.setObjectName(u"progress_analyze")
        # self.progress_analyze.setValue(0)
        self.progress_analyze.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.progress_analyze)

        self.label_load = QLabel(self.tab_load)
        self.label_load.setObjectName(u"label_load")

        self.verticalLayout.addWidget(self.label_load)
        self.tabWidget.addTab(self.tab_load, "")

        # tab initial table
        # C:\\Users\\Пользователь\\Downloads\\
        # df = pd.read_excel("C:\\Users\\Пользователь\\Downloads\\Координаты движения мыши Unix mini.xlsx")
        # df = df.reset_index()

        # Table bot/unbot
        self.tab_table_init = QWidget()
        self.verticalLayout_tab_init = QVBoxLayout()
        self.verticalLayout_tab_init.setObjectName(u"verticalLayout_tab_init")
        self.verticalLayout_tab_init.setContentsMargins(10, 10, 10, 10)
        self.tab_table_init.setObjectName(u"tab_table_init")
        self.tab_table_init.setGeometry(QRect(30, 10, 981, 551))

        self.label_table_init = QLabel()
        self.label_table_init.setObjectName(u"label_table_init")
        self.label_table_init.setVisible(False)
        self.verticalLayout_tab_init.addWidget(self.label_table_init)

        self.tab_table_init.setLayout(self.verticalLayout_tab_init)

        self.tableWidget_init = STableWidet(checkbox_list=['ID'], rows_per_page=1000,
                                            filter_only_if_return_pressed=True)
        self.verticalLayout_tab_init.addWidget(self.tableWidget_init)
        self.tabWidget.addTab(self.tab_table_init, "Таблица с ботами")

        self.but_plot_trajectories = QPushButton()
        self.but_plot_trajectories.setObjectName(u"but_plot_trajectories")
        self.but_plot_trajectories.setVisible(False)
        self.verticalLayout_tab_init.addWidget(self.but_plot_trajectories)

        self.but_save_tab_init = QPushButton()
        self.but_save_tab_init.setObjectName(u"but_plot_trajectories")
        self.but_save_tab_init.setText("Сохранить таблицу с ботами")
        self.but_save_tab_init.setVisible(False)
        self.verticalLayout_tab_init.addWidget(self.but_save_tab_init)

        #  plot track session
        self.tab_plot_trajectories = QWidget()
        self.verticalLayout_tab_plot_traj = QVBoxLayout()
        self.tab_plot_trajectories.setLayout(self.verticalLayout_tab_plot_traj)
        self.tabWidget.addTab(self.tab_plot_trajectories, "График траекторий")
        self.matplotlib_traj_widget = MatplotlibWidget(figure=None)
        self.verticalLayout_tab_plot_traj.addWidget(self.matplotlib_traj_widget)

        # tab Table users
        self.tab_table_user = QWidget()
        self.verticalLayout_tab_users = QVBoxLayout()
        self.verticalLayout_tab_users.setContentsMargins(10, 10, 10, 10)
        self.tab_table_user.setObjectName(u"tab_table_user")

        self.label_user = QLabel(self.tab_table_user)
        self.label_user.setObjectName(u"label_user")
        self.label_user.setVisible(False)
        self.label_user.setGeometry(QRect(20, 20, 351, 17))
        self.verticalLayout_tab_users.addWidget(self.label_user)

        self.tab_table_user.setLayout(self.verticalLayout_tab_users)

        self.tableWidget_users = STableWidet(checkbox_list=['ACCOUNT_ID'], rows_per_page=1000,
                                             filter_only_if_return_pressed=False)
        self.verticalLayout_tab_users.addWidget(self.tableWidget_users)
        self.tabWidget.addTab(self.tab_table_user, "Таблица по пользователям")

        self.horizontalLayout_tab_users = QHBoxLayout()

        self.but_plot_tsne = QPushButton()
        self.but_plot_tsne.setObjectName(u"but_plot_trajectories")
        self.but_plot_tsne.setText("Построить график кластеризации")
        self.but_plot_tsne.setVisible(False)
        self.horizontalLayout_tab_users.addWidget(self.but_plot_tsne)

        self.but_filtred_users = QPushButton()
        self.but_filtred_users.setObjectName(u"but_plot_trajectories")
        self.but_filtred_users.setText("Отобразить сессии выбранных пользователей")
        self.but_filtred_users.setVisible(False)
        self.horizontalLayout_tab_users.addWidget(self.but_filtred_users)

        self.verticalLayout_tab_users.addLayout(self.horizontalLayout_tab_users)

        self.but_save_tab_users = QPushButton()
        self.but_save_tab_users.setObjectName(u"but_plot_trajectories")
        self.but_save_tab_users.setText("Сохранить таблицу с кластеризацией")
        self.but_save_tab_users.setVisible(False)
        self.verticalLayout_tab_users.addWidget(self.but_save_tab_users)

        # plot clusterization
        self.tab_plot_tsne = QWidget()
        self.verticalLayout_tab_plot_tsne = QVBoxLayout()
        self.tab_plot_tsne.setLayout(self.verticalLayout_tab_plot_tsne)
        self.tabWidget.addTab(self.tab_plot_tsne, "График кластеризации")
        self.matplotlib_tsne_widget = MatplotlibWidget(figure=None)
        self.verticalLayout_tab_plot_tsne.addWidget(self.matplotlib_tsne_widget)

        # tab table sessions
        self.tab_table_session = QWidget()
        self.verticalLayout_tab_sessions = QVBoxLayout()
        self.verticalLayout_tab_sessions.setContentsMargins(10, 10, 10, 10)
        self.tab_table_session.setObjectName(u"tab_table_session")
        self.label_sessions = QLabel(self.tab_table_session)
        self.label_sessions.setObjectName(u"label_sessions")
        self.label_sessions.setVisible(False)
        self.label_sessions.setGeometry(QRect(30, 20, 351, 17))
        self.verticalLayout_tab_sessions.addWidget(self.label_sessions)
        self.tab_table_session.setLayout(self.verticalLayout_tab_sessions)

        self.tableWidget_sessions = STableWidet(checkbox_list=None, rows_per_page=1000,
                                                filter_only_if_return_pressed=False)
        self.verticalLayout_tab_sessions.addWidget(self.tableWidget_sessions)
        self.tabWidget.addTab(self.tab_table_session, "Таблица по сессиям")

        self.verticalLayout_central.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1041, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.but_load_excel.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0444\u0430\u0439\u043b excel", None))
        self.but_analyze.setText(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0430\u043b\u0438\u0437 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.but_clusterize.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u044f", None))
        self.label_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u0432 \u0444\u043e\u0440\u043c\u0430\u0442\u0435 excel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_load), QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_table_init.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0438\u0441\u0445\u043e\u0434\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.but_plot_trajectories.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u0442\u0440\u0430\u0435\u043a\u0442\u043e\u0440\u0438\u0439", None))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_table_init), QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430", None))
        self.label_user.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0441 \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u0435\u0439 \u043f\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_table_user), QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u043f\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c", None))
        self.label_sessions.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0441 \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u0435\u0439 \u043f\u043e \u0441\u0435\u0441\u0441\u0438\u044f\u043c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_table_session), QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u043f\u043e \u0441\u0435\u0441\u0441\u0438\u044f\u043c", None))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plot_trajectories), QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444\u0438\u043a\u0438 \u0442\u0440\u0430\u0435\u043a\u0442\u043e\u0440\u0438\u0439", None))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plot_clusters), QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444\u0438\u043a\u0438 \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u043e\u0432", None))
    # retranslateUi

