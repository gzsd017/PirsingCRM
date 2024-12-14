import sqlite3
from PyQt5 import QtWidgets


class OpenTable:
    def __init__(self, db_file, table_widget):
        self.db_file = db_file
        self.table_widget = table_widget
        self.current_table = None

    def open_table_from_db(self, table_name):
        self.current_table = table_name
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()

            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(column_names))
            self.table_widget.setHorizontalHeaderLabels(column_names)

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.table_widget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col_data)))

            if "ID" in column_names:
                id_col_index = column_names.index("ID")
                self.table_widget.setColumnHidden(id_col_index, True)

            self.table_widget.setVisible(True)

            column_widths = {
                "Клиенты": [475, 475, 478],
                "Услуги": [475, 475, 478],
                "Материал": [475, 475, 478],
                "Мастер": [475, 475, 478],
                "Расписание": [237] * 6,
                "Комплекты": [237] * 6
            }

            for col_idx, width in enumerate(column_widths.get(table_name, [])):
                self.table_widget.setColumnWidth(col_idx + 1, width)

        except Exception as e:
            print(f"Возникла ошибка: {e}")
        finally:
            connection.close()