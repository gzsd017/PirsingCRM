import sqlite3
from PyQt5 import QtWidgets

class OpenTable:
    def __init__(self, db_file, table_widget):
        self.db_file = db_file
        self.table_widget = table_widget
        self.current_table = None

    def fetch_data(self, query):
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(query)
            data = [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            data = []
        finally:
            connection.close()
        return data

    def create_combobox(self, items, current_value=None):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        if current_value and current_value in items:
            combo.setCurrentText(current_value)
        return combo

    def clear_table(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)

    def open_table_from_db(self, table_name):
        self.current_table = table_name
        self.clear_table()  # Очистка таблицы перед загрузкой новых данных
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
                    column_name = column_names[col_idx]

                    if table_name == "Расписание":
                        if column_name == "Клиент":
                            items = self.fetch_data("SELECT Имя FROM Клиенты")
                            combo = self.create_combobox(items, current_value=str(col_data))
                            self.table_widget.setCellWidget(row_idx, col_idx, combo)
                        elif column_name == "Услуга":
                            items = self.fetch_data("SELECT Название FROM Услуги")
                            combo = self.create_combobox(items, current_value=str(col_data))
                            self.table_widget.setCellWidget(row_idx, col_idx, combo)
                        elif column_name == "Мастер":
                            items = self.fetch_data("SELECT Имя FROM Мастер")
                            combo = self.create_combobox(items, current_value=str(col_data))
                            self.table_widget.setCellWidget(row_idx, col_idx, combo)
                        else:
                            item = QtWidgets.QTableWidgetItem(str(col_data))
                            self.table_widget.setItem(row_idx, col_idx, item)
                    elif table_name == "Услуги" and column_name == "Материал":
                        items = self.fetch_data("SELECT Название FROM Материал")
                        combo = self.create_combobox(items, current_value=str(col_data))
                        self.table_widget.setCellWidget(row_idx, col_idx, combo)
                    elif table_name == "Комплекты" and column_name.startswith("Материал"):
                        items = self.fetch_data("SELECT Название FROM Материал")
                        combo = self.create_combobox(items, current_value=str(col_data))
                        self.table_widget.setCellWidget(row_idx, col_idx, combo)
                    else:
                        item = QtWidgets.QTableWidgetItem(str(col_data))
                        self.table_widget.setItem(row_idx, col_idx, item)

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

        except sqlite3.Error as e:
            print(f"Ошибка при открытии таблицы {table_name}: {e}")
        finally:
            connection.close()

    def save_changes_to_db(self):
        if self.current_table is None:
            print("Таблица не выбрана для сохранения данных.")
            return

        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()

            column_names = [self.table_widget.horizontalHeaderItem(i).text() for i in
                            range(self.table_widget.columnCount())]

            for row in range(self.table_widget.rowCount()):
                record = []
                for col in range(self.table_widget.columnCount()):
                    if isinstance(self.table_widget.cellWidget(row, col), QtWidgets.QComboBox):
                        item = self.table_widget.cellWidget(row, col).currentText()
                    else:
                        item = self.table_widget.item(row, col).text() if self.table_widget.item(row, col) else None
                    record.append(item)

                id_value = record[0]
                if id_value:
                    set_clause = ', '.join([f'{column_names[i]} = ?' for i in range(1, len(record))])
                    cursor.execute(f"UPDATE {self.current_table} SET {set_clause} WHERE ID = ?",
                                   (*record[1:], id_value))
                else:
                    placeholders = ', '.join(['?'] * len(record))
                    cursor.execute(
                        f"INSERT INTO {self.current_table} ({', '.join(column_names)}) VALUES ({placeholders})", record)

            connection.commit()
            print("Изменения успешно сохранены.")
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении изменений: {e}")
        finally:
            connection.close()




