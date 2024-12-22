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
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.table_widget.setItem(row_idx, col_idx, item)

                    if column_names[col_idx] in ["Услуга", "Материал"]:
                        combo_box = QtWidgets.QComboBox()
                        combo_box.addItems(["Option 1", "Option 2"])
                        self.table_widget.setCellWidget(row_idx, col_idx, combo_box)

            if "ID" in column_names:
                id_col_index = column_names.index("ID")
                self.table_widget.setColumnHidden(id_col_index, True)

            self.table_widget.setVisible(True)

            column_widths = {
                "Клиенты": [475, 475, 478],
                "Услуги": [475, 475, 478],
                "Материал": [475, 475, 478],
                "Мастер": [475, 475, 478],
                "Расписание": [237] * 7,
                "Комплекты": [237] * 6
            }

            for col_idx, width in enumerate(column_widths.get(table_name, [])):
                self.table_widget.setColumnWidth(col_idx, width)

        except Exception as e:
            print(f"Возникла ошибка: {e}")
        finally:
            connection.close()

    def save_changes_to_db(self):
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()

            for row in range(self.table_widget.rowCount()):
                record = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    record.append(item.text() if item else None)

                # Предполагаем, что первая колонка - это ID
                id_value = record[0]
                if id_value is not None:
                    # Обновление существующей записи
                    cursor.execute(f"UPDATE {self.current_table} SET {', '.join([f'column_{i} = ?' for i in range(1, len(record))])} WHERE ID = ?", (*record[1:], id_value))
                else:
                    # Добавление новой записи
                    placeholders = ', '.join(['?'] * len(record))
                    cursor.execute(f"INSERT INTO {self.current_table} VALUES ({placeholders})", record)

            connection.commit()
        except Exception as e:
            print(f"Ошибка при сохранении изменений: {e}")
        finally:
            connection.close()