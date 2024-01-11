from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QLabel, QTabWidget


class STableWidet(QWidget):
    """
    dataframe - датафрейм для анализа
    checkbox_list - список названий колонок, в которых проставить чекбоксы
    rows_per_page - количество записей на 1 странице таблицы
    filter_only_if_return_pressed - фильтровать только по нажатии enter
    """
    def __init__(self,
                 dataframe,
                 checkbox_list=None,
                 rows_per_page=1000,
                 filter_only_if_return_pressed=False):
        super().__init__()
        if checkbox_list is None:
            checkbox_list = []
        self.df = dataframe
        self.filtering = False
        self.current_page = 0
        self.default_rows_per_page = rows_per_page
        self.rows_per_page = self.default_rows_per_page
        self.checkbox_list = checkbox_list

        self._initialize_ui(filter_only_if_return_pressed)

    def _initialize_ui(self, filter_only_if_return_pressed):
        external_layout = QVBoxLayout()
        external_layout.setAlignment(Qt.AlignCenter)

        self.filter_line_edits = []
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(0)
        for column in self.df.columns:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Фильтр {column}")
            if filter_only_if_return_pressed:
                line_edit.returnPressed.connect(self._filter_table)
                line_edit.textChanged.connect(self._stop_filter_table)
            else:
                line_edit.textChanged.connect(self._filter_table)

            line_edit.setFixedWidth(100)
            self.filter_line_edits.append(line_edit)
            filter_layout.addWidget(line_edit)

        filter_layout.addStretch(1)

        external_layout.addLayout(filter_layout)

        self.table_widget = QTableWidget()
        external_layout.addWidget(self.table_widget)

        self.table_widget.setColumnCount(len(self.df.columns))
        self.table_widget.setRowCount(len(self.df))

        self.table_widget.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                item = QTableWidgetItem(str(self.df.iloc[i, j]))

                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                if self.df.columns[j] in self.checkbox_list:
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)

                self.table_widget.setItem(i, j, item)

        self.table_widget.horizontalHeader().sectionResized.connect(self._on_column_resized)
        self.table_widget.setSortingEnabled(True)

        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.verticalHeader().setFixedWidth(self.table_widget.verticalHeader().width())
        self._add_padding_to_filters(self.table_widget.verticalHeader().width(), filter_layout)

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

        self._update_table()

        self.setWindowTitle("Статистическая таблица)")

        self.setLayout(external_layout)

    @staticmethod
    def _add_padding_to_filters(width, filter_layout):
        filter_layout.setContentsMargins(width, 0, 0, 0)

    def _on_column_resized(self, idx, prev_size, new_size):
        self.filter_line_edits[idx].setFixedWidth(new_size)

    def _update_table(self):
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
                note = self.table_widget.item(row, col)

                if text and text not in note.text().lower():
                    hide_row = True
                    break
            if hide_row is False:
                length += 1
            self.table_widget.setRowHidden(row, hide_row)
        self.rows_per_page = length
        self._update_page_num_line(filtering=True)

    def get_index_of_selected_items(self):
        # функция для возвращения индексов чекбокснутых записей
        selected_indices = []
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                if self.table_widget.item(row, col).checkState() == Qt.Checked:
                    selected_indices.append(row)
                    break
        return selected_indices

    def get_values_of_selected_items(self):
        # функция для возвращения чекбокснутых значений
        return self.df.loc[self.get_index_of_selected_items(), self.checkbox_list]
