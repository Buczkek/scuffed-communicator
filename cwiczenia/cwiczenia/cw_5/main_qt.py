from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget
import sys


class SubWindow(QWidget):
    emitMsg = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        self.setup()
    def akcja(self):
        self.emitMsg.emit(self.wejscie.text())
        print("ok")

    def setup(self):
        self.etykieta = QLabel('Wpisz:', self)
        self.wejscie = QLineEdit()
        #self.wynik = QLineEdit()
        self.button1 = QPushButton('Wyślij dane', self)
        self.button1.clicked.connect(self.akcja)
       
        uklad = QGridLayout()
        uklad.addWidget(self.etykieta, 0, 0)
        uklad.addWidget(self.wejscie, 0, 1)
        #uklad.addWidget(self.wynik, 1, 0, 1, 2)
        uklad.addWidget(self.button1, 2, 0, 1, 2)
        #uklad.addWidget(self.button2, 2, 1)

        self.setLayout(uklad)
        self.setGeometry(20, 20, 300, 100)
        self.setWindowTitle("Drugie okna")

        #self.show()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.subWindow = SubWindow()
        self.subWindow.emitMsg.connect(self.showMsg)
        self.setup()

    def akcja(self):
        nadawca = self.sender()
        if nadawca.text() == "Wciśnij mnie":

            dane = self.wejscie.text()
            QMessageBox.warning(self, "Komunikat", dane, QMessageBox.Ok)
        else:
            self.subWindow.show()

    def showMsg(self, msg):
        self.wynik.setText(msg)

    def setup(self):
        self.etykieta = QLabel('Wpisz tekst:', self)
        self.wejscie = QLineEdit()
        self.wynik = QLineEdit()
        self.button1 = QPushButton('Wciśnij mnie', self)
        self.button1.clicked.connect(self.akcja)
        self.button2 = QPushButton('Mnie też', self)
        self.button2.clicked.connect(self.akcja)

        uklad = QGridLayout()
        uklad.addWidget(self.etykieta, 0, 0)
        uklad.addWidget(self.wejscie, 0, 1)
        uklad.addWidget(self.wynik, 1, 0, 1, 2)
        uklad.addWidget(self.button1, 2, 0)
        uklad.addWidget(self.button2, 2, 1)

        self.setLayout(uklad)
        self.setGeometry(20, 20, 300, 100)
        self.setWindowTitle("Okno 1")

        self.show()


app = QApplication(sys.argv)
window = MainWindow()

sys.exit(app.exec_())
