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

        MainWindow.setCentralWidget(self.centralwidget)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), MainWindow)
        self.shortcut.activated.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.db_manager = OpenTable('CRM.db', self.table_widget)
        self.crud_manager = CRUD('CRM.db')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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

    def create_combobox(self):
        self.combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box.setGeometry(QtCore.QRect(430, 50, 300, 30))
        self.combo_box.addItems(["Расписание", "Клиенты", "Услуга", "Материал", "Мастер", "Комплекты"])
        #self.combo_box.currentIndexChanged.connect(self.change_table)

    def create_buttons(self):
        button_specs = [
            ("Расписание", (10, 110), "Расписание"),
            ("Клиенты", (10, 180), "Клиенты"),
            ("Услуги", (10, 250), "Услуги"),
            ("Материалы", (10, 320), "Материал"),
            ("Финансы", (10, 530), "Финансы"),
            ("Мастер", (10, 460), "Мастер"),
            ("Комплекты", (10, 390), "Комплекты"),
            ("Добавить", (430, 100), "dob"),
            ("Редактировать", (700, 100), "red"),
            ("Удалить", (970, 100), "delit")
        ]

        for text, position, name in button_specs:
            button = QtWidgets.QPushButton(self.centralwidget)
            if name in ["dob", "red", "delit"]:
                button.setGeometry(QtCore.QRect(*position, 260, 58))
            else:
                button.setGeometry(QtCore.QRect(*position, 375, 61))
            button.setStyleSheet(self.button_style())
            button.setText(text)
            button.setObjectName(name)

            if name == "dob":
                #button.clicked.connect(self.add_record)
                pass
            elif name == "red":
                #button.clicked.connect(self.edit_record)
                pass
            elif name == "delit":
                #button.clicked.connect(self.delete_record)
                pass
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
        self.calend.setDate(QtCore.QDate(2024, 12, 20))
        self.calend.setObjectName("calend")

    def create_table_widget(self):
        self.table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.table_widget.setGeometry(QtCore.QRect(438, 180, 1430, 900))
        self.table_widget.setStyleSheet(self.table_widget_style())
        self.table_widget.setVisible(False)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
