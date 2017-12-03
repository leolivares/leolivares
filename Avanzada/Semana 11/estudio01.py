from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.Qt import QTest

from random import sample
from events import Mostrar

class Ventana(QWidget):

    trigger_mostrar = pyqtSignal(Mostrar)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memoria")
        self.setGeometry(100, 100, 300, 400)

        self.vbox = QVBoxLayout(self)

        self.botones = []

        self.fila1 = QHBoxLayout(self)
        self.fila2 = QHBoxLayout(self)
        self.fila3 = QHBoxLayout(self)
        self.fila4 = QHBoxLayout(self)
        self.fila5 = QHBoxLayout(self)

        self.vbox.addLayout(self.fila1)
        self.vbox.addLayout(self.fila2)
        self.vbox.addLayout(self.fila3)
        self.vbox.addLayout(self.fila4)
        self.vbox.addLayout(self.fila5)

        self.set_inicial()
        self.cartas = self.asignar_cartas()
        self.back_end = Tablero(self.cartas)

        self.trigger_mostrar.connect(self.back_end.voltear_carta)

        self.show()

    def set_inicial(self):
        i = 0
        for _ in range(0, 25):

            print(i)
            if _ % 5  == 0 and _ != 25:
                i += 1

            filas = {1: self.fila1, 2: self.fila2, 3: self.fila3,
                     4: self.fila4, 5: self.fila5}

            self.button = QPushButton(self)
            self.botones.append(self.button)
            #self.image.setPixmap(QPixmap("car.jpg").scaled(450 / 3, 300 / 3))
            #self.image.setFixedSize(160, 130)
            imagen = QIcon(QPixmap("car.jpg").scaled(450 / 3, 450/ 3))

            self.button.clicked.connect(self.presionar)

            self.button.setIcon(imagen)
            self.button.setIconSize(QSize(50, 50))
            fila = filas[i]
            fila.addWidget(self.button)

    def asignar_cartas(self):
        numeros = ["1" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                   "12", "b", "back"]

        orden = sample(numeros, len(numeros))
        cartas = []
        botones = sample(self.botones, len(self.botones))
        for num, bot in zip(orden, botones):
            cartas.append(Carta(num + ".png", bot))
        return cartas

    def presionar(self):

        boton = self.sender()
        self.trigger_mostrar.emit(Mostrar(boton))


class Carta:

    def __init__(self, nombre, boton):
        self.nombre = nombre
        self.boton = boton


class Tablero:

    def __init__(self, cartas):
        self.cartas = cartas

    def voltear_carta(self, boton):
        for carta in self.cartas:
            if carta.boton == boton.boton:
                carta.boton.hide()




if __name__ == '__main__':
    app = QApplication([])
    window = Ventana()
    app.exec_()
