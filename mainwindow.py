from PyQt5 import QtCore, QtGui, QtWidgets
from open_table import OpenTable
from crud import CRUD

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(83, 173, 155); border-color: rgb(85, 255, 0);")
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.create_vertical_line()
        self.create_label()
        self.create_buttons()
        self.create_calendar()
        self.create_table_widget()
        self.create_financial_fields()

        MainWindow.setCentralWidget(self.centralwidget)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), MainWindow)
        self.shortcut.activated.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.db_manager = OpenTable('CRM.db', self.table_widget)
        self.crud_manager = CRUD('CRM.db')

        # Загрузка данных из базы данных при старте
        self.load_data_from_db()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Информационная система для пирсинг-салона"))
        self.label.setText(_translate("MainWindow", "Информационная система для пирсинг-салона"))

    def create_vertical_line(self):
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(270, 0, 250, 1080))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

    def create_label(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 261, 61))
        self.label.setMaximumSize(QtCore.QSize(261, 16777215))
        font = QtGui.QFont("Bahnschrift", 14)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0); font: 75 15pt 'Bahnschrift';")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

    def create_buttons(self):
        button_specs = [
            ("Расписание", (10, 110), "Расписание"),
            ("Клиенты", (10, 180), "Клиенты"),
            ("Услуги", (10, 250), "Услуги"),
            ("Материал", (10, 320), "Материал"),
            ("Финансы", (10, 530), "finances"),
            ("Мастер", (10, 460), "Мастер"),
            ("Комплекты", (10, 390), "Комплекты"),
            ("Добавить", (430, 100), "dob"),
            ("Редактировать", (700, 100), "red"),
            ("Удалить", (970, 100), "delit")
        ]

        for text, position, name in button_specs:
            button = QtWidgets.QPushButton(self.centralwidget)
            button.setGeometry(QtCore.QRect(*position, 260 if name in ["dob", "red", "delit"] else 375, 58))
            button.setStyleSheet(self.button_style())
            button.setText(text)
            button.setObjectName(name)

            if name == "dob":
                button.clicked.connect(self.add_empty_row)
            elif name == "red":
                button.clicked.connect(self.edit_record)  # Обработчик редактирования
            elif name == "delit":
                button.clicked.connect(self.confirm_delete_record)
            elif name == "finances":
                button.clicked.connect(self.show_financials)
            else:
                button.clicked.connect(lambda _, b=text: self.open_table_from_db(b))

    def button_style(self):
        return """
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
        """

    def create_calendar(self):
        self.calend = QtWidgets.QDateEdit(self.centralwidget)
        self.calend.setGeometry(QtCore.QRect(425, 21, 1450, 61))
        self.calend.setStyleSheet("background-color: rgb(255, 255, 255); font: 75 16pt 'Bahnschrift';")
        self.calend.setDate(QtCore.QDate.currentDate())
        self.calend.setObjectName("calend")

    def create_table_widget(self):
        self.table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.table_widget.setGeometry(QtCore.QRect(438, 180, 1430, 900))
        self.table_widget.setStyleSheet(self.table_widget_style())
        self.table_widget.setVisible(False)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

    def create_financial_fields(self):
        self.income_label = QtWidgets.QLabel(self.centralwidget)
        self.income_label.setGeometry(QtCore.QRect(10, 600, 400, 30))
        self.income_label.setText("Доходы: 0")
        self.income_label.setStyleSheet(self.financial_label_style())
        
        self.expense_label = QtWidgets.QLabel(self.centralwidget)
        self.expense_label.setGeometry(QtCore.QRect(10, 640, 400, 30))
        self.expense_label.setText("Расходы: 0")
        self.expense_label.setStyleSheet(self.financial_label_style())
        
        self.material_balance_label = QtWidgets.QLabel(self.centralwidget)
        self.material_balance_label.setGeometry(QtCore.QRect(10, 680, 400, 30))
        self.material_balance_label.setText("Остаток материалов: 0")
        self.material_balance_label.setStyleSheet(self.financial_label_style())

        # Скрываем метки доходов и расходов изначально
        self.income_label.setVisible(False)
        self.expense_label.setVisible(False)
        self.material_balance_label.setVisible(False)

    def financial_label_style(self):
        return """
            color: rgb(0, 100, 0);  /* Темно-зеленый цвет для доходов */
            font: 75 18pt 'Bahnschrift';
            background-color: rgba(255, 255, 255, 0.7); /* Полупрозрачный фон */
            border: 1px solid rgb(0, 100, 0); /* Темно-зеленая рамка */
            padding: 5px;
            border-radius: 5px; /* Закругленные углы */
        """

    def table_widget_style(self):
        return """
            QTableWidget {
                background-color: rgb(255, 255, 255);
                font: 12pt 'Bahnschrift';
                gridline-color: rgb(200, 200, 200);
            }
            QHeaderView::section {
                background-color: rgb(173, 216, 230);
                color: rgb(0, 0, 0);
                font: bold 14pt 'Bahnschrift';
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: rgb(100, 150, 200);
                color: white;
            }
        """

    def open_table_from_db(self, table_name):
        self.db_manager.open_table_from_db(table_name)

    def add_empty_row(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

    def edit_record(self):
        row_position = self.table_widget.currentRow()
        if row_position >= 0:
            record_id = self.table_widget.item(row_position, 0).text()
            # Здесь нужно добавить логику для редактирования записи
            print(f"Editing record with ID: {record_id}")

    def show_financials(self):
        self.calculate_finances()

        # Показываем метки доходов и расходов
        self.income_label.setVisible(True)
        self.expense_label.setVisible(True)
        self.material_balance_label.setVisible(True)

    def calculate_finances(self):
        try:
            income = self.crud_manager.read_records("Услуги")
            total_income = sum(float(record["price"]) for record in income)

            expenses = self.crud_manager.read_records("Материал")
            total_expense = sum(float(record["cost"]) for record in expenses)

            materials = self.crud_manager.read_records("Материал")
            total_materials = sum(float(record["purchased"]) for record in materials) - sum(float(record["used"]) for record in materials)

            self.income_label.setText(f"Доходы: {total_income:.2f}")
            self.expense_label.setText(f"Расходы: {total_expense:.2f}")
            self.material_balance_label.setText(f"Остаток материалов: {total_materials:.2f}")

        except Exception as e:
            print(f"Ошибка при расчете финансов: {e}")

    def confirm_delete_record(self):
        row_position = self.table_widget.currentRow()
        if row_position >= 0:
            record_id = self.table_widget.item(row_position, 0).text()
            reply = QtWidgets.QMessageBox.question(None, 'Подтверждение удаления',
                                                   "Точно удалить?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                # Удаление записи из всех таблиц
                tables_to_delete = ["Расписание", "Клиенты", "Мастер", "Материал", "Комплекты"]
                for table in tables_to_delete:
                    self.crud_manager.delete_record(table, record_id)
                self.table_widget.removeRow(row_position)

    def load_data_from_db(self):
        # Здесь загружаем данные из базы данных в таблицу
        records = self.crud_manager.read_records("Материал")  # Замените на нужную таблицу
        self.table_widget.setRowCount(0)  # Очищаем таблицу перед загрузкой новых данных

        for record in records:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for column_index, value in enumerate(record):
                self.table_widget.setItem(row_position, column_index, QtWidgets.QTableWidgetItem(str(value)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
