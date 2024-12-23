import sqlite3
from PyQt5 import QtWidgets, QtCore

class DatabaseComboDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, db_file, combo_type, parent=None):
        super().__init__(parent)
        self.db_file = db_file
        self.combo_type = combo_type
        self.data_list = self.fetch_data()

    def fetch_data(self):
        if self.combo_type == "Клиент":
            query = "SELECT Имя FROM Клиенты"
        elif self.combo_type == "Услуга":
            query = "SELECT Название FROM Услуги"
        elif self.combo_type == "Мастер":
            query = "SELECT Имя FROM Мастер"
        else:
            return []

        data = []
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(query)
            data = [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
        finally:
            connection.close()
        return data

    def createEditor(self, parent, option, index):
        combo = QtWidgets.QComboBox(parent)
        combo.addItems(self.data_list)
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        if value in self.data_list:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), QtCore.Qt.EditRole)


class OpenTable:
    def __init__(self, db_file, table_widget):
        self.db_file = db_file
        self.table_widget = table_widget
        self.current_table = None

    def clear_table(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)

    def open_table_from_db(self, table_name):
        self.current_table = table_name
        self.clear_table()
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

            if "ID" in column_names:
                id_col_index = column_names.index("ID")
                self.table_widget.setColumnHidden(id_col_index, True)

            self.table_widget.setVisible(True)

            for col_idx, col_name in enumerate(column_names):
                if col_name in ["Клиент", "Услуга", "Мастер"]:
                    delegate = DatabaseComboDelegate(self.db_file, col_name, self.table_widget)
                    self.table_widget.setItemDelegateForColumn(col_idx, delegate)

        except sqlite3.Error as e:
            print(f"Ошибка при открытии таблицы {table_name}: {e}")
        finally:
            connection.close()

    def add_new_row(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        for col in range(self.table_widget.columnCount()):
            item = QtWidgets.QTableWidgetItem("")
            self.table_widget.setItem(row_position, col, item)

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
                    item = self.table_widget.item(row, col).text() if self.table_widget.item(row, col) else None
                    record.append(item)

                print(f"Обрабатываем запись: {record}")
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









