import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.editing_row_index = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(83, 173, 155); border-color: rgb(85, 255, 0);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(270, 0, 250, 1080))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 261, 61))
        font = QtGui.QFont("Bahnschrift", 14, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0); font: 75 15pt 'Bahnschrift';")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        button_style = """
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

        self.dob = QtWidgets.QPushButton(self.centralwidget)
        self.dob.setGeometry(QtCore.QRect(430, 100, 250, 50))
        self.dob.setStyleSheet(button_style)
        self.dob.setObjectName("dob")

        self.red = QtWidgets.QPushButton(self.centralwidget)
        self.red.setGeometry(QtCore.QRect(700, 100, 250, 50))
        self.red.setStyleSheet(button_style)
        self.red.setObjectName("red")

        self.delit = QtWidgets.QPushButton(self.centralwidget)
        self.delit.setGeometry(QtCore.QRect(970, 100, 250, 50))
        self.delit.setStyleSheet(button_style)
        self.delit.setObjectName("delit")

        menu_buttons = [
            ("rasp", "Расписание", 10, 110),
            ("clien", "Клиенты", 10, 180),
            ("usl", "Услуги", 10, 250),
            ("mat", "Материалы", 10, 320),
            ("komp", "Комплекты", 10, 390),
            ("mast", "Мастер", 10, 460),
            ("fin", "Финансы", 10, 530),
        ]

        for obj_name, text, x, y in menu_buttons:
            button = QtWidgets.QPushButton(self.centralwidget)
            button.setGeometry(QtCore.QRect(x, y, 375, 61))
            button.setStyleSheet(button_style)
            button.setObjectName(obj_name)
            button.setText(text)
            setattr(self, obj_name, button)

        self.calend = QtWidgets.QDateEdit(self.centralwidget)
        self.calend.setGeometry(QtCore.QRect(425, 21, 1450, 61))
        self.calend.setStyleSheet("background-color: rgb(255, 255, 255); font: 75 16pt 'Bahnschrift';")
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
        """)
        self.table_widget.setVisible(False)
        self.table_widget.setObjectName("table_widget")

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), MainWindow)
        self.shortcut.activated.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Информационная система для пирсинг-салона"))
        self.label.setText(_translate("MainWindow", "Информационная система для пирсинг-салона"))
        self.dob.setText(_translate("MainWindow", "Добавить"))
        self.red.setText(_translate("MainWindow", "Редактировать"))
        self.delit.setText(_translate("MainWindow", "Удалить"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
