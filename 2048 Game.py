from random import randint
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication #, QLabel, QPushButton
from PyQt5 import QtGui, QtCore, QtWidgets

class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.colors = {
            '.': QtGui.QColor(0xcdc1b4),
            2: QtGui.QColor(0xeee4da),
            4: QtGui.QColor(0xede0c8),
            8: QtGui.QColor(0xf2b179),
            16: QtGui.QColor(0xf59563),
            32: QtGui.QColor(0xf67c5f),
            64: QtGui.QColor(0xf65e3b),
            128: QtGui.QColor(0xedcf72),
            256: QtGui.QColor(0xedcc61),
            512: QtGui.QColor(0xedc850),
            1024: QtGui.QColor(0xedc53f),
            2048: QtGui.QColor(0xedc22e),
            4096: QtGui.QColor(0xedc690e)
        }
        self.initUI()

        self.n = 5
        self.best = 0
        self.create_field()
        self.rand_cord()

    def initUI(self):
        self.setGeometry(300, 300, 420, 500)
        self.setWindowTitle('2048')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        elif e.key() == QtCore.Qt.Key_Up:
            Game.pocess_rotate(self, 'w')
            self.Play()
        elif e.key() == QtCore.Qt.Key_Down:
            Game.pocess_rotate(self, 's')
            self.Play()
        elif e.key() == QtCore.Qt.Key_Left:
            Game.pocess_rotate(self, 'a')
            self.Play()
        elif e.key() == QtCore.Qt.Key_Right:
            Game.pocess_rotate(self, 'd')
            self.Play()

    def mousePressEvent(self, e):
        self.lastPoint = e.pos()

    def mouseReleaseEvent(self, e):
        self.resetField = QtCore.QRect(220, 15, 80, 60)
        self.openMenu = QtCore.QRect(320, 15, 80, 60)
        if self.resetField.contains(self.lastPoint.x(), self.lastPoint.y()):
            self.Game_over()

        if self.openMenu.contains(self.lastPoint.x(), self.lastPoint.y()):
            self.start_menu = Start_Menu()
            self.close()

    def create_field(self):
        self.check = [True, True, True]
        self.win = False
        self.score = 0
        self.a = [['.']*self.n for i in range(self.n)] # Не создаэ силку на строки

    def rand_cord(self):
        self.chis = [2, 4]
        if self.check[0] or self.check[1]:
            self.value = randint(0,1)
            self.cord = [randint(0, (self.n) - 1), randint(0, (self.n) - 1)]
            while self.a[self.cord[0]][self.cord[1]] != '.':
                self.cord = [randint(0, (self.n) - 1), randint(0, (self.n) - 1)]
            self.a[self.cord[0]][self.cord[1]] = self.chis[self.value]

            for i in range(self.n):
                for j in range(self.n):
                    print(self.a[i][j], end = '\t')
                print('\n')
            print()

    def Game_over(self):
        if QtWidgets.QMessageBox.question(self, 'Message',"Do You Want To Restart ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes:
            self.create_field()
            self.rand_cord()
        else:
            sys.exit()

    def You_win(self):
        if not self.win and self.win2 >= 1:
            self.win = True
            if QtWidgets.QMessageBox.question(self, 'You Win', "Do You Want To Restart ?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                              QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes:
                self.create_field()
                self.rand_cord()

    def Play(self):
        self.check = []
        self.move()
        self.add()
        self.move()
        self.rotate(4 - self.N)
        self.rand_cord()
        self.Check()
        self.You_win()

    def pocess_rotate(self, N):
        wsad = {'w': 0, 'd': 3, 's': 2, 'a': 1}
        self.N = wsad[N] # поворот масиву n раз
        self.rotate(self.N)

    def rotate(self, N):
        ''' 1) Розвертає наш список, щоб можна було використовувати 1 умову по переміщенню'''
        for i in range(N):
            y = [row[:] for row in self.a]  # clone a
            for i in range(self.n):
                for j in range(self.n):
                    self.a[i][self.n-1 - j] = y[j][i]

    def add(self):
        self.count = False
        ''' 2)Додає цифри в полі гри'''
        for i in range(self.n - 1): #index 0 to 2 because i+1
            for j in range(self.n): # index 0 to 3
                if self.a[i][j] != '.' and self.a[i][j] == self.a[i+1][j]:
                    self.a[i][j] += self.a[i+1][j]
                    self.score += self.a[i][j]
                    self.a[i+1][j] = '.'
                    self.count = True
                    if self.score >= self.best:
                        self.best = self.score
        self.check.append(self.count)

    def move(self):
        ''' 3) Переміщає цифри в полі гри'''
        self.count = False
        for b in range(self.n - 1): # 1 проход 1 переміщення
            for i in range(self.n - 1): #index 0 to 2 because i+1
                for j in range(self.n): # index 0 to 3
                    if self.a[i][j] == '.' and self.a[i+1][j] != '.':
                        self.a[i][j] = self.a[i+1][j]
                        self.a[i+1][j] = '.'
                        self.count = True
        self.check.append(self.count)

    def Check(self):
        self.summa = sum(i.count('.') for i in self.a)
        self.win2 = sum(i.count(2048) for i in self.a)
        if self.win2 >= 1:
            self.win2 = True
        self.lose = []
        for i in range(4):
            a = [row[:] for row in self.a]  # clone a
            self.Check_add(a, i)
        if not (True in self.lose) and self.summa == 0:
            self.Game_over()

    def Check_add(self, a, N):
        count = False
        for i in range(N):
            y = [row[:] for row in a]  # clone a
            for i in range(self.n):
                for j in range(self.n):
                    a[i][self.n-1 - j] = y[j][i]

        for i in range(self.n - 1): #index 0 to 2 because i+1
            for j in range(self.n): # index 0 to 3
                if a[i][j] != '.' and a[i][j] == a[i+1][j]:
                    a[i][j] += a[i+1][j]
                    a[i+1][j] = '.'
                    count = True
        self.lose.append(count)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0xbbada0)))
        painter.drawRect(self.rect())

        painter.setBrush(QtGui.QBrush(QtGui.QColor(0x776e65)))
        painter.drawRoundedRect(QtCore.QRect(20, 15, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 12))
        painter.setPen(QtGui.QColor(0xcdc1b4))
        painter.drawText(QtCore.QRectF(QtCore.QRect(20, 20, 80, 60)), "SCORE",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter))
        painter.setFont(QtGui.QFont("Arial", 18))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(20, 15, 80, 55)), str(self.score),
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom))
        painter.setPen(QtCore.Qt.NoPen)

        painter.drawRoundedRect(QtCore.QRect(120, 15, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 12))
        painter.setPen(QtGui.QColor(0xcdc1b4))
        painter.drawText(QtCore.QRectF(QtCore.QRect(120, 20, 80, 60)), "BEST",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter))
        painter.setFont(QtGui.QFont("Arial", 18))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(120, 15, 80, 55)), str(self.best),
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom))
        painter.setPen(QtCore.Qt.NoPen)

        painter.drawRoundedRect(QtCore.QRect(220, 15, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 16))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(220, 15, 80, 60)), "RESET",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setPen(QtCore.Qt.NoPen)

        painter.drawRoundedRect(QtCore.QRect(320, 15, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 16))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(320, 15, 80, 60)), "MENU",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setPen(QtCore.Qt.NoPen)

        self.drawRectangles(painter)

    def drawRectangles(self, painter):
        for i in range(self.n):
            for j in range(self.n):
                painter.setFont(QtGui.QFont("Arial", 20, 10))
                painter.setBrush(QtGui.QColor(self.colors[self.a[i][j]]))
                painter.drawRoundedRect(QtCore.QRect(20 + j * 80, 90 + i * 80, 60, 60), 10, 10)
                if self.a[i][j] == '.':
                    painter.setPen(QtCore.Qt.NoPen)
                else:
                    painter.setPen(QtGui.QColor(100, 100, 100))

                painter.drawText(QtCore.QRectF(QtCore.QRect(20 + j * 80, 90 + i * 80, 60, 60)), str(self.a[i][j]),
                                 QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
                painter.setPen(QtCore.Qt.NoPen)

                self.update()

class Start_Menu(QMainWindow):
    '''Стартове меню гри'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 420, 500)
        self.setWindowTitle('2048')
        self.show()

    def mousePressEvent(self, e):
        self.lastPoint = e.pos()

    def mouseReleaseEvent(self, e):
        self.openStart = QtCore.QRect(170, 150, 80, 60)
        self.openOption = QtCore.QRect(170, 230, 80, 60)
        if self.openStart.contains(self.lastPoint.x(), self.lastPoint.y()):
            self.game = Game()
            self.close()

        if self.openOption.contains(self.lastPoint.x(), self.lastPoint.y()):
            self.option = Option()
            self.close()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0xbbada0)))
        painter.drawRect(self.rect())

        painter.setBrush(QtGui.QBrush(QtGui.QColor(0x776e65)))
        painter.drawRoundedRect(QtCore.QRect(170, 150, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 16))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(170, 150, 80, 60)), "START",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setPen(QtCore.Qt.NoPen)

        painter.drawRoundedRect(QtCore.QRect(170, 230, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 16))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(170, 230, 80, 60)), "OPTION",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setPen(QtCore.Qt.NoPen)

    def start(self):
        self.Game = Game()
        self.close()

    def option(self):
        self.Option = Option()
        self.close()

class Option(QMainWindow):
    '''Опції гри'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 420, 500)
        self.setWindowTitle('2048')
        self.show()

    def mousePressEvent(self, e):
        self.lastPoint = e.pos()

    def mouseReleaseEvent(self, e):
        self.openMenu = QtCore.QRect(170, 150, 80, 60)
        if self.openMenu.contains(self.lastPoint.x(), self.lastPoint.y()):
            self.start_menu = Start_Menu()
            self.close()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0xbbada0)))
        painter.drawRect(self.rect())

        painter.setBrush(QtGui.QBrush(QtGui.QColor(0x776e65)))
        painter.drawRoundedRect(QtCore.QRect(170, 150, 80, 60), 5, 5)
        painter.setFont(QtGui.QFont("Arial", 16))
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(QtCore.QRectF(QtCore.QRect(170, 150, 80, 60)), "MENU",
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setPen(QtCore.Qt.NoPen)

    def menu(self):
        self.Start_Menu = Start_Menu()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Menu()
    sys.exit(app.exec_())