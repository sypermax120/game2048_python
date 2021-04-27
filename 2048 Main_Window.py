import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import QtCore, QtGui

class Start_Menu(QMainWindow):
    '''Стартове меню гри'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        Start = QPushButton("Start", self)
        Start.move(100, 200)

        Option = QPushButton("Option", self)
        Option.move(100, 250)

        Start.clicked.connect(self.start)
        Option.clicked.connect(self.option)

        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('2048')
        self.show()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0xbbada0)))
        painter.drawRect(self.rect())

    def start(self):
        self.Game = Game()
        self.close()

    def option(self):
        self.Option = Option()
        self.close()

class Game(QMainWindow):
    '''Ігрове поле'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        Menu = QPushButton("Menu", self)
        Menu.move(45, 5)

        Reset = QPushButton("Reset", self)
        Reset.move(155, 5)

        Menu.clicked.connect(self.menu)
        Reset.clicked.connect(self.initUI)

        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('2048')
        self.show()

    def menu(self):
        self.Start_Menu = Start_Menu()
        self.close()

class Option(QMainWindow):
    '''Опції гри'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        Menu = QPushButton("Menu", self)
        Menu.move(195, 5)
        Menu.clicked.connect(self.menu)

        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('2048')
        self.show()

    def menu(self):
        self.Start_Menu = Start_Menu()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Menu()
    sys.exit(app.exec_())