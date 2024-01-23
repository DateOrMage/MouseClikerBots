import sys
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QLabel, QTabWidget, QFileDialog, QSpacerItem, QSizePolicy, QHeaderView


class STableWidet(QWidget):
    """
    dataframe - датафрейм для анализа
    checkbox_list - список названий колонок, в которых проставить чекбоксы
    rows_per_page - количество записей на 1 странице таблицы
    filter_only_if_return_pressed - фильтровать только по нажатии enter
    """
    def __init__(self,
                 dataframe=None,
                 checkbox_list=None,
                 rows_per_page=1000,
                 filter_only_if_return_pressed=False):
        super().__init__()

        if checkbox_list is None:
            checkbox_list = []

        if dataframe is None:
            dataframe = pd.DataFrame()

        self.df = dataframe
        self.filtering = False
        self.current_page = 0
        self.default_rows_per_page = rows_per_page
        self.rows_per_page = self.default_rows_per_page
        self.checkbox_list = checkbox_list
        self.filter_only_if_pressed = filter_only_if_return_pressed
        self.selected_items = []
        self.ui_created = False


        self._initialize_ui()



    def _initialize_ui(self):
        external_layout = QVBoxLayout()

        # Лэйаут для полей фильтрации
        self.filter_line_edits = []
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setSpacing(0)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        # self.filter_layout.set

        self._set_filter_edits()

        external_layout.addLayout(self.filter_layout)

        # Виджет для таблицы
        self.table_widget = QTableWidget()
        self.table_widget.itemChanged.connect(self._check_cell)
        self.table_widget.horizontalHeader().sectionResized.connect(self._on_column_resized)
        #self.table_widget.verticalHeader().setFixedWidth(self.table_widget.verticalHeader().width())
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSortingEnabled(True)

        self._set_table()

        external_layout.addWidget(self.table_widget)



        page_num_layout = QHBoxLayout()
        self.page_num_prev = QPushButton("Предыдущая страница")
        self.page_num_prev.clicked.connect(self._prev_page)

        self.page_num_line = QLabel()
        self._update_page_num_line()

        self.page_num_next = QPushButton("Следующая страница")
        self.page_num_next.clicked.connect(self._next_page)

        page_num_layout.addWidget(self.page_num_prev, 1)
        page_num_layout.addWidget(self.page_num_line, 1)
        page_num_layout.addWidget(self.page_num_next, 1)

        external_layout.addLayout(page_num_layout)

        # #закоментить
        # loadPushButton = QPushButton("загрузить")
        # loadPushButton.clicked.connect(self.load_df)
        # external_layout.addWidget(loadPushButton)
        # #закоментить

        self._update_table()

        self.setWindowTitle("Статистическая таблица)")
        external_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(external_layout)

    #закоментить
    # def load_df(self):
    #     options = QFileDialog.Options()
    #     filePath, _ = QFileDialog.getOpenFileName(self, "Выберите файл Excel", "", "Excel Files (*.xlsx)", options=options)
    #
    #     if filePath:
    #         df = pd.read_excel(filePath)
    #
    #     self.set_dataframe(df)
    #закоменить

    def _on_column_resized(self, idx, prev_size, new_size):
        self.filter_line_edits[idx].setFixedWidth(new_size)

    def _update_table(self):
        #self.table_widget.sortItems(0, Qt.SortOrder.AscendingOrder)
        start_row = self.current_page * self.rows_per_page
        if start_row + self.rows_per_page < len(self.df):
            end_row = start_row + self.rows_per_page
        else:
            end_row = len(self.df)
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHidden(row, not (start_row <= row < end_row))
        self._update_page_num_line()

    def _next_page(self):
        if self.filtering:
            return
        if (self.current_page + 1) * self.rows_per_page < len(self.df):
            self.current_page += 1
            self._update_table()

    def _prev_page(self):
        if self.filtering:
            return
        if self.current_page > 0:
            self.current_page -= 1
            self._update_table()

    def _update_page_num_line(self, filtering=False):
        start_row = self.current_page * self.rows_per_page + 1
        end_row = min(start_row + self.rows_per_page - 1, len(self.df))
        max_pages = end_row if filtering else len(self.df)
        self.page_num_line.setText(f"{start_row}...{end_row} / {max_pages}")

    def _stop_filter_table(self):
        continue_flag = False
        for line_edit in self.filter_line_edits:
            if len(line_edit.text()) != 0:
                continue_flag = True

        if continue_flag is False:
            self.current_page = 0
            self.rows_per_page = self.default_rows_per_page
            self.filtering = False
            self._update_table()
            return True

    def _filter_table(self):
        if self._stop_filter_table():
            return

        self.filtering = True
        length = 0
        for row in range(self.table_widget.rowCount()):
            hide_row = False
            for col, line_edit in enumerate(self.filter_line_edits):

                text = line_edit.text().lower()
                value = self.table_widget.item(row, col).text()

                try:
                    text = text.replace(",", ".")
                    chars_before_dot = value.find('.')
                    if chars_before_dot == -1:
                        num_of_chars = 0
                    else:
                        num_of_chars = 6 - chars_before_dot
                        if num_of_chars < 0:
                            num_of_chars = 0
                    value = float(value)
                    format_string = "{:." + str(num_of_chars) + "f}"
                    value = format_string.format(value)
                    value = str(float(value))
                except:
                    pass

                if text and text not in value.lower():
                    hide_row = True
                    break
            if hide_row is False:
                length += 1
            self.table_widget.setRowHidden(row, hide_row)
        self.rows_per_page = length
        self._update_page_num_line(filtering=True)

    def _set_filter_edits(self):
        def clearLayout(layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        clearLayout(self.filter_layout)

        self.filter_line_edits = []
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        for column in self.df.columns:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Фильтр {column}")
            if self.filter_only_if_pressed:
                line_edit.returnPressed.connect(self._filter_table)
                line_edit.textChanged.connect(self._stop_filter_table)
            else:
                line_edit.textChanged.connect(self._filter_table)

            #line_edit.setFixedWidth(100)
            self.filter_line_edits.append(line_edit)
            self.filter_layout.addWidget(line_edit)

        #self.filter_layout.addStretch(2)
        #spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.filter_layout.addSpacerItem(spacer)
        self.filter_layout.addStretch(1)

    def _set_table(self):
        self.selected_items = []

        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)

        self.table_widget.setColumnCount(len(self.df.columns))
        self.table_widget.setRowCount(len(self.df))

        self.table_widget.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):

                if pd.api.types.is_numeric_dtype(self.df[self.df.columns[j]]):
                    # print(self.df[self.df.columns[j]].dtype)
                    item = QTableWidgetItem()
                    if 'int' in str(type(self.df.iloc[i, j])):
                    #item.setData(Qt.DisplayRole, int(self.df.iloc[i, j]))
                        item.setData(Qt.EditRole, int(self.df.iloc[i, j]))
                    else:
                        item.setData(Qt.EditRole, float(self.df.iloc[i, j]))

                else:
                    item = QTableWidgetItem(str(self.df.iloc[i, j]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                if self.df.columns[j] in self.checkbox_list:
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)

                self.table_widget.setItem(i, j, item)


        self.table_widget.resizeColumnsToContents()

        self.ui_created = True


    def _check_cell(self, item):

        if self.ui_created is False:
            return

        if item.checkState() == Qt.Checked and item not in self.selected_items:
            self.selected_items.append(item)
        elif item.checkState() == Qt.Unchecked and item in self.selected_items:
            self.selected_items.remove(item)


    def set_dataframe(self, dataframe):
        self.ui_created = False

        self.df = dataframe

        self._set_filter_edits()

        self._set_table()

        self._update_table()


    # def get_index_of_selected_items(self):
    #     # функция для возвращения индексов чекбокснутых записей
    #     selected_indices = []
    #     for row in range(self.table_widget.rowCount()):
    #         for col in range(self.table_widget.columnCount()):
    #             if self.table_widget.item(row, col).checkState() == Qt.Checked:
    #                 selected_indices.append(row)
    #                 break
    #     return selected_indices

    def get_values_of_selected_items(self):
        # функция для возвращения чекбокснутых значений
        # return self.df.loc[self.get_index_of_selected_items(), self.checkbox_list[0]].values
        checked_items = []

        for item in self.selected_items:
            checked_items.append(item.text())

        for item in self.selected_items:
            item.setCheckState(Qt.Unchecked)

        return checked_items


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tab = QTabWidget()
    tab.resize(950, 500)
    df = pd.read_excel('/Users/danielageev/Work/AI BMSTU/other/НОТАРИУС/analyzed_data.xlsx', index_col=None)
    # df = pd.read_excel('200тыс_записей_20231115_Выгрузка_координат_с_временем_для_анализа.xlsx')
    df_users = df.groupby('ACCOUNT_ID').sum().reset_index()
    tab.addTab(
        STableWidet(),
        "таблица сессии"
    )

    tab.addTab(
        STableWidet(df_users,
                    checkbox_list=['ACCOUNT_ID'],
                    rows_per_page=500,
                    filter_only_if_return_pressed=True),
        "таблица пользователи"
    )

    tab.show()
    sys.exit(app.exec())