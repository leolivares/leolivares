from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.Qt import QTest
from eventos import Ingreso, Apostar
import time
from eventos import Ingreso
from random import randint

class TragaMonedas(QObject):

    trigger_respuesta_ingreso = pyqtSignal(Ingreso)
    trigger_respuesta_apostar = pyqtSignal(Apostar)

    def __init__(self, parent):
        super().__init__()
        self.usuarios = list()
        self.cargar_personas()

        self.trigger_respuesta_ingreso.connect(parent.comenzar)
        self.trigger_respuesta_apostar.connect(parent.apostar1)


    def cargar_personas(self):
        with open("usuarios_registrados.txt", "a+") as archivo:
            self.usuarios = [Usuario(*line.strip().split(","))
                             for line in archivo]


    def ingreso(self, event):
        nombre = event.usuario

        usuario = list(filter(lambda x: x.nombre == nombre, self.usuarios))

        if len(usuario) != 0:
            usu = usuario[0]
        else:
            usu = Usuario(nombre, 1500, 0, 0)

        self.trigger_respuesta_ingreso.emit(Ingreso(usu))

    def apostar(self, event):

        cantidad = event.cant
        usuario = event.usuario
        imagenes = [randint(1, 3), randint(1, 3), randint(1, 3)]

        if not 2 in imagenes and not 3 in imagenes:
            factor = 2
        elif not 1 in imagenes and not 3 in imagenes:
            factor = 1.5
        elif not 1 in imagenes and not 2 in imagenes:
            factor = 1.25
        elif 1 in imagenes:
            factor = 0.9
        elif imagenes.count(2) == 2:
            factor = 0.8

        else:
            factor = 0

        usuario.saldo += factor * cantidad
        imagenes_str = [str(i) + ".png" for i in imagenes]

        event.imagenes = imagenes_str

        self.trigger_respuesta_apostar.emit(Apostar(usuario, cantidad, imagenes_str))




class Usuario:

    def __init__(self, nombre, saldo, ult_apuesta, max_apuesta):
        self.nombre = nombre
        self.saldo = saldo
        self.ult_apuesta = ult_apuesta
        self.max_apuesta = max_apuesta

