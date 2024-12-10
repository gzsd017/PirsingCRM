from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_MainWindow(object):
    def __init__(self):
        self.editing_row_index = None
        self.is_editing = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(83, 173, 155); border-color: rgb(85, 255, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(270, 0, 250, 1080))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 261, 61))
        self.label.setMaximumSize(QtCore.QSize(261, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"Bahnschrift\";")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.dob = QtWidgets.QPushButton(self.centralwidget)
        self.dob.setGeometry(QtCore.QRect(430, 100, 250, 50))
        self.dob.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 204, 199);
                font: 75 16pt "Bahnschrift";
            }
            QPushButton:hover {
                background-color: rgb(220, 170, 170);
            }
            QPushButton:pressed {
                background-color: rgb(180, 140, 140);
            }
        """)
        self.dob.setObjectName("clien")
        self.dob.clicked.connect(self.add_empty_row)

        self.red = QtWidgets.QPushButton(self.centralwidget)
        self.red.setGeometry(QtCore.QRect(700, 100, 250, 50))
        self.red.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.red.setObjectName("clien")
        self.red.clicked.connect(self.toggle_edit_mode)

        self.delit = QtWidgets.QPushButton(self.centralwidget)
        self.delit.setGeometry(QtCore.QRect(970, 100, 250, 50))
        self.delit.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.delit.clicked.connect(self.delete_data_from_db)

        self.rasp = QtWidgets.QPushButton(self.centralwidget)
        self.rasp.setGeometry(QtCore.QRect(10, 110, 375, 61))
        self.rasp.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.rasp.clicked.connect(lambda: self.open_table_from_db("Расписание"))

        self.clien = QtWidgets.QPushButton(self.centralwidget)
        self.clien.setGeometry(QtCore.QRect(10, 180, 375, 61))
        self.clien.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.clien.setObjectName("clien")
        self.clien.clicked.connect(lambda: self.open_table_from_db("Клиенты"))

        self.usl = QtWidgets.QPushButton(self.centralwidget)
        self.usl.setGeometry(QtCore.QRect(10, 250, 375, 61))
        self.usl.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.usl.setObjectName("usl")
        self.usl.clicked.connect(lambda: self.open_table_from_db("Услуги"))

        self.mat = QtWidgets.QPushButton(self.centralwidget)
        self.mat.setGeometry(QtCore.QRect(10, 320, 375, 61))
        self.mat.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.mat.setObjectName("mat")
        self.mat.clicked.connect(lambda: self.open_table_from_db("Материал"))

        self.fin = QtWidgets.QPushButton(self.centralwidget)
        self.fin.setGeometry(QtCore.QRect(10, 530, 375, 61))
        self.fin.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.fin.setObjectName("fin")
        self.fin.clicked.connect(lambda: self.open_table_from_db("Финансы"))

        self.mast = QtWidgets.QPushButton(self.centralwidget)
        self.mast.setGeometry(QtCore.QRect(10, 460, 375, 61))
        self.mast.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.mast.setObjectName("mast")
        self.mast.clicked.connect(lambda: self.open_table_from_db("Мастер"))

        self.komp = QtWidgets.QPushButton(self.centralwidget)
        self.komp.setGeometry(QtCore.QRect(10, 390, 375, 61))
        self.komp.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 204, 199);
                        font: 75 16pt "Bahnschrift";
                    }
                    QPushButton:hover {
                        background-color: rgb(220, 170, 170);
                    }
                    QPushButton:pressed {
                        background-color: rgb(180, 140, 140);
                    }
                """)
        self.komp.setObjectName("komp")
        self.komp.clicked.connect(lambda: self.open_table_from_db("Комплекты"))

        self.calend = QtWidgets.QDateEdit(self.centralwidget)
        self.calend.setGeometry(QtCore.QRect(425, 21, 1450, 61))
        self.calend.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 16pt \"Bahnschrift\";")
        self.calend.setDate(QtCore.QDate(2024, 12, 20))
        self.calend.setObjectName("calend")

        self.table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.table_widget.setGeometry(QtCore.QRect(438, 180, 1430, 900))
        self.table_widget.setStyleSheet("""
                    QTableWidget {
                        background-color: rgb(255, 255, 255);
                        font: 12pt 'Bahnschrift';
                        gridline-color: rgb(200, 200, 200);
                    }
                    QHeaderView::section {
                        background-color: rgb(173, 216, 230); /* Легкий голубой фон для заголовков */
                        color: rgb(0, 0, 0); /* Черный текст */
                        font: bold 14pt 'Bahnschrift'; /* Полужирный шрифт */
                        padding: 5px; /* Отступы для заголовков */
                    }
                    QTableWidget::item {
                        padding: 5px; /* Отступ в ячейках */
                    }
                    QTableWidget::item:selected {
                        background-color: rgb(100, 150, 200); /* Цвет выделенной ячейки */
                        color: white; /* Цвет текста для выделенной ячейки */
                    }
                """)
        self.table_widget.setVisible(False)
        self.table_widget.itemChanged.connect(self.save_data_to_db)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


        MainWindow.setCentralWidget(self.centralwidget)

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), MainWindow)
        self.shortcut.activated.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Информационная система для пирсинг-салона"))
        self.rasp.setText(_translate("MainWindow", "Расписание"))
        self.clien.setText(_translate("MainWindow", "Клиенты"))
        self.usl.setText(_translate("MainWindow", "Услуги"))
        self.mat.setText(_translate("MainWindow", "Материалы"))
        self.fin.setText(_translate("MainWindow", "Финансы"))
        self.mast.setText(_translate("MainWindow", "Мастер"))
        self.komp.setText(_translate("MainWindow", "Комплекты"))
        self.dob.setText(_translate("MainWindow", "Добавить"))
        self.red.setText(_translate("MainWindow", "Редактировать"))
        self.delit.setText(_translate("MainWindow", "Удалить"))

    def open_table_from_db(self, table_name):
        self.current_table = table_name
        try:
            connection = sqlite3.connect('CRM.db')
            cursor = connection.cursor()

            try:
                if table_name == "Клиенты":
                    query = "SELECT Имя || ' - ' || Телефон AS Клиент FROM Клиенты"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    column_names = ["Клиент"]

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

                for col_idx in range(len(column_names)):

                    if table_name == "Расписание":
                        self.table_widget.setColumnWidth(1, 237)
                        self.table_widget.setColumnWidth(2, 237)
                        self.table_widget.setColumnWidth(3, 237)
                        self.table_widget.setColumnWidth(4, 237)
                        self.table_widget.setColumnWidth(5, 237)
                        self.table_widget.setColumnWidth(6, 237)

                    if table_name == "Комплекты":
                        self.table_widget.setColumnWidth(1, 237)
                        self.table_widget.setColumnWidth(2, 237)
                        self.table_widget.setColumnWidth(3, 237)
                        self.table_widget.setColumnWidth(4, 237)
                        self.table_widget.setColumnWidth(5, 237)
                        self.table_widget.setColumnWidth(6, 237)

                    if table_name == "Клиенты":
                        self.table_widget.setColumnWidth(1, 475)
                        self.table_widget.setColumnWidth(2, 475)
                        self.table_widget.setColumnWidth(3, 478)

                    if table_name == "Услуги":
                        self.table_widget.setColumnWidth(1, 475)
                        self.table_widget.setColumnWidth(2, 475)
                        self.table_widget.setColumnWidth(3, 478)

                    if table_name == "Материал":
                        self.table_widget.setColumnWidth(1, 475)
                        self.table_widget.setColumnWidth(2, 475)
                        self.table_widget.setColumnWidth(3, 478)

                    if table_name == "Мастер":
                        self.table_widget.setColumnWidth(1, 475)
                        self.table_widget.setColumnWidth(2, 475)
                        self.table_widget.setColumnWidth(3, 478)

            except Exception as e:
                print(f"Ошибка при выполнении запроса: {e}")

        except Exception as e:
            print(f"Возникла ошибка: {e}")
        finally:
            connection.close()

    def add_empty_row(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

    def toggle_edit_mode(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            return

        if self.is_editing:
            self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.is_editing = False

        else:
            self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed)  
            self.table_widget.editItem(self.table_widget.item(selected_row, 1))
            self.is_editing = True

    def save_data_to_db(self, item):
        if item:
            row = item.row()
            current_table = self.current_table

            try:
                connection = sqlite3.connect('CRM.db')
                cursor = connection.cursor()

                unique_id_item = self.table_widget.item(row,
                                                        0)
                unique_id = unique_id_item.text() if unique_id_item else None

                if current_table == "Клиенты":
                    name = self.table_widget.item(row, 1)
                    surname = self.table_widget.item(row, 2)
                    phone = self.table_widget.item(row, 3)

                    if name and surname and phone:
                        if unique_id:
                            cursor.execute("UPDATE Клиенты SET Имя = ?, Фамилия = ?, Телефон = ? WHERE id = ?",
                                           (name.text(), surname.text(), phone.text(), unique_id))
                            connection.commit()
                            print("Данные успешно обновлены в таблице 'Клиенты'.")
                        else:
                            cursor.execute("INSERT INTO Клиенты (Имя, Фамилия, Телефон) VALUES (?, ?, ?)",
                                           (name.text(), surname.text(), phone.text()))
                            connection.commit()
                            print("Данные успешно сохранены в таблицу 'Клиенты'.")


                elif current_table == "Услуги":
                    name = self.table_widget.item(row, 1)
                    price = self.table_widget.item(row, 2)
                    material = self.table_widget.item(row, 3)
                    if name and price and material:
                        if unique_id:
                            cursor.execute("UPDATE Услуги SET Название = ?, Цена = ?, Материал = ? WHERE id = ?",
                                           (name.text(), float(price.text()), material.text(), unique_id))
                            connection.commit()
                            print("Данные успешно обновлены в таблице 'Услуги'.")
                        else:
                            cursor.execute("INSERT INTO Услуги (Название, Цена, Материал) VALUES (?, ?, ?)",
                                           (name.text(), float(price.text()), material.text()))
                            connection.commit()
                            print("Данные успешно сохранены в таблицу 'Услуги'.")

                elif current_table == "Мастер":
                    name = self.table_widget.item(row, 1)
                    surname = self.table_widget.item(row, 2)
                    phone = self.table_widget.item(row, 3)
                    if name and surname and phone:
                        if unique_id:
                            cursor.execute("UPDATE Мастер SET Имя = ?, Фамилия = ?, Телефон = ? WHERE id = ?",
                                           (name.text(), surname.text(), phone.text(), unique_id))
                            connection.commit()
                            print("Данные успешно обновлены в таблице 'Мастер'.")
                        else:
                            cursor.execute("INSERT INTO Мастер (Имя, Фамилия, Телефон) VALUES (?, ?, ?)",
                                           (name.text(), surname.text(), phone.text()))
                            connection.commit()
                            print("Данные успешно сохранены в таблицу 'Мастер'.")

                elif current_table == "Расписание":
                    client_name = self.table_widget.item(row, 1)
                    service_name = self.table_widget.item(row, 2)
                    price = self.table_widget.item(row, 3)
                    master_name = self.table_widget.item(row, 4)
                    appointment_date = self.table_widget.item(row, 5)
                    appointment_time = self.table_widget.item(row, 6)

                    if client_name and service_name and price and master_name and appointment_date and appointment_time:
                        try:
                            price_value = float(price.text())
                            if unique_id:
                                cursor.execute("""
                                                UPDATE Расписание 
                                                SET Клиент = ?, Услуга = ?, Цена = ?, Мастер = ?, Дата = ?, Время = ?
                                                WHERE id = ?
                                            """,
                                               (
                                               client_name.text(), service_name.text(), price_value, master_name.text(),
                                               appointment_date.text(), appointment_time.text(), unique_id))
                                connection.commit()
                                print("Данные успешно обновлены в таблице 'Расписание'.")
                            else:
                                cursor.execute(
                                    "INSERT INTO Расписание (Клиент, Услуга, Цена, Мастер, Дата, Время) VALUES (?, ?, ?, ?, ?, ?)",
                                    (client_name.text(), service_name.text(), price_value, master_name.text(),
                                     appointment_date.text(), appointment_time.text()))
                                connection.commit()
                                print("Данные успешно сохранены в таблицу 'Расписание'.")

                        except ValueError:
                            print("Ошибка: Неверное значение цены. Пожалуйста, введите числовое значение.")


                elif current_table == "Комплекты":
                    package_number = self.table_widget.item(row, 1)
                    material1 = self.table_widget.item(row, 2)
                    material2 = self.table_widget.item(row, 3)
                    material3 = self.table_widget.item(row, 4)
                    material4 = self.table_widget.item(row, 5)
                    material5 = self.table_widget.item(row, 6)
                    if package_number and material1 and material2 and material3 and material4 and material5:
                        if unique_id:
                            cursor.execute("""
                                            UPDATE Комплекты 
                                            SET Номер = ?, Материал1 = ?, Материал2 = ?, Материал3 = ?, Материал4 = ?, Материал5 = ?
                                            WHERE id = ?
                                        """,
                                           (package_number.text(), material1.text(), material2.text(), material3.text(),
                                            material4.text(), material5.text(), unique_id))
                            connection.commit()
                            print("Данные успешно обновлены в таблице 'Комплекты'.")
                        else:
                            cursor.execute(
                                "INSERT INTO Комплекты (Номер, Материал1, Материал2, Материал3, Материал4, Материал5) VALUES (?, ?, ?, ?, ?, ?)",
                                (package_number.text(), material1.text(), material2.text(), material3.text(),
                                 material4.text(), material5.text()))
                            connection.commit()
                            print("Данные успешно сохранены в таблицу 'Комплекты'.")


                elif current_table == "Материал":
                    material_name = self.table_widget.item(row, 1)
                    price = self.table_widget.item(row, 2)
                    quantity = self.table_widget.item(row, 3)
                    if material_name and price and quantity:
                        if unique_id:
                            cursor.execute("""
                                            UPDATE Материал 
                                            SET Название = ?, Цена = ?, Количество = ?
                                            WHERE id = ?
                                        """,
                                           (material_name.text(), float(price.text()), int(quantity.text()), unique_id))
                            connection.commit()
                            print("Данные успешно обновлены в таблице 'Материал'.")
                        else:
                            cursor.execute(
                                "INSERT INTO Материал (Название, Цена, Количество) VALUES (?, ?, ?)",
                                (material_name.text(), float(price.text()), int(quantity.text())))
                            connection.commit()
                            print("Данные успешно сохранены в таблицу 'Материал'.")

            except Exception as e:
                print(f"Ошибка при сохранении данных в базу: {e}")
            finally:
                connection.close()

    def delete_data_from_db(self):
        current_table = self.current_table
        selected_row = self.table_widget.currentRow()

        if selected_row >= 0:
            try:
                connection = sqlite3.connect('CRM.db')
                cursor = connection.cursor()

                if current_table == "Клиенты":
                    phone = self.table_widget.item(selected_row, 3)
                    if phone:
                        cursor.execute("DELETE FROM Клиенты WHERE Телефон = ?", (phone.text(),))
                        print("Клиент успешно удален.")

                elif current_table == "Услуги":
                    service_name = self.table_widget.item(selected_row,
                                                          1)
                    if service_name:
                        cursor.execute("DELETE FROM Услуги WHERE Название = ?", (service_name.text(),))
                        print("Услуга успешно удалена.")

                elif current_table == "Материал":
                    material_name = self.table_widget.item(selected_row,
                                                          1)
                    if material_name:
                        cursor.execute("DELETE FROM Материал WHERE Название = ?", (material_name.text(),))
                        print("Материал успешно удален.")

                elif current_table == "Комплекты":
                    complect_name = self.table_widget.item(selected_row,
                                                          1)
                    if complect_name:
                        cursor.execute("DELETE FROM Комплекты WHERE Номер = ?", (complect_name.text(),))
                        print("Комплект успешно удален.")

                elif current_table == "Мастер":
                    master_name = self.table_widget.item(selected_row,
                                                         1)
                    if master_name:
                        cursor.execute("DELETE FROM Мастер WHERE Имя = ?", (master_name.text(),))
                        print("Мастер успешно удален.")

                elif current_table == "Расписание":
                    master_id = self.table_widget.item(selected_row, 4)
                    service_id = self.table_widget.item(selected_row, 2)
                    date_time = self.table_widget.item(selected_row, 6)
                    if master_id and service_id and date_time:
                        cursor.execute("DELETE FROM Расписание WHERE Мастер = ? AND Услуга = ? AND Время = ?",
                                       (master_id.text(), service_id.text(), date_time.text()))
                        print("Запись расписания успешно удалена.")

                connection.commit()

                self.table_widget.removeRow(selected_row)
                print("Строка успешно удалена из таблицы приложения.")

            except Exception as e:
                print(f"Произошла ошибка: {e}")

            finally:
                connection.close()
        else:
            print("Выберите строку для удаления.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(MainWindow.windowFlags() | QtCore.Qt.FramelessWindowHint)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




