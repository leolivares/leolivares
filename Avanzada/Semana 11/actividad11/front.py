from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.Qt import QTest
from eventos import Ingreso, Apostar
from back import TragaMonedas
import time


class Ventana(QWidget):

    trigger_ingreso = pyqtSignal(Ingreso)
    trigger_apuesta = pyqtSignal(Apostar)

    def __init__(self):
        super().__init__()
        self.monto_apuesta = 0
        self.usuario_actual = None
        self.runUi()


    def runUi(self):

        self.back_end = TragaMonedas(self)

        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle("Walking Luddite")

        self.vbox = QVBoxLayout(self)

        self.label_nombre = QLabel("Ingresar tu nombre de usuario", self)
        self.line_edit = QLineEdit(self)
        self.boton_entrar = QPushButton("Ingresar", self)
        self.boton_entrar.clicked.connect(self.ingresar)

        self.horiz = QHBoxLayout(self)
        self.vbox.addStretch(1)

        self.horiz.addWidget(self.line_edit)
        self.horiz.addWidget(self.boton_entrar)

        self.vbox.addWidget(self.label_nombre)
        self.vbox.addLayout(self.horiz)

        self.show()

        self.trigger_ingreso.connect(self.back_end.ingreso)
        self.trigger_apuesta.connect(self.back_end.apostar)

    def comenzar(self, evento):
        usuario = evento.usuario
        self.usuario_actual = usuario

        self.setGeometry(100, 100, 300, 200)

        self.nombre_layout = QHBoxLayout(self)
        self.info_layout = QHBoxLayout(self)
        self.tragamonedas_layout = QHBoxLayout(self)
        self.apuesta_layout = QHBoxLayout(self)

        self.info_div1 = QVBoxLayout(self)


        self.label_nombre = QLabel("Hola {}".format(usuario.nombre), self)
        self.nombre_layout.addWidget(self.label_nombre)

        self.info_layout.addLayout(self.info_div1)


        self.info_div11 = QHBoxLayout(self)
        self.info_div12 = QHBoxLayout(self)

        self.info_div1.addLayout(self.info_div11)
        self.info_div1.addLayout(self.info_div12)

        self.label_max = QLabel("Maximo premio ganado", self)
        self.label_cant_max = QLabel("{}".format(usuario.max_apuesta), self)
        self.label_ult_apuesta = QLabel("Ultima Apuesta", self)
        self.label_num = QLabel("{}".format(usuario.ult_apuesta), self)

        self.info_div11.addWidget(self.label_max)
        self.info_div11.addWidget(self.label_cant_max)
        self.info_div12.addWidget(self.label_ult_apuesta)
        self.info_div12.addWidget(self.label_num)

        self.label_saldo = QLabel("Saldo", self)
        self.label_cant_saldo = QLabel("{}".format(usuario.saldo), self)

        self.info_layout.addWidget(self.label_saldo)
        self.info_layout.addWidget(self.label_cant_saldo)

        self.image1 = QLabel(self)
        self.image1.setPixmap(QPixmap("imagenes/0.png").scaled(100, 100))
        self.image1.setFixedSize(160, 130)

        self.image2 = QLabel(self)
        self.image2.setPixmap(QPixmap("imagenes/0.png").scaled(100, 100))
        self.image2.setFixedSize(160, 130)

        self.image3 = QLabel(self)
        self.image3.setPixmap(QPixmap("imagenes/0.png").scaled(100, 100))
        self.image3.setFixedSize(160, 130)

        self.boton_apostar = QPushButton("Apostar!", self)
        self.boton_apostar.clicked.connect(self.realizar_apuesta)

        self.tragamonedas_layout.addWidget(self.image1)
        self.tragamonedas_layout.addWidget(self.image2)
        self.tragamonedas_layout.addWidget(self.image3)
        self.tragamonedas_layout.addWidget(self.boton_apostar)


        self.label_apuesta_actual = QLabel("Apuesta Actual", self)
        self.cant_apuesta_actual = QLabel("{}".format(self.monto_apuesta), self)

        self.div_botones_layout = QVBoxLayout(self)
        self.boton_mas = QPushButton("+", self)
        self.boton_menos = QPushButton("-", self)

        self.boton_mas.clicked.connect(self.aumentar)
        self.boton_menos.clicked.connect(self.disminuir)

        self.div_botones_layout.addWidget(self.boton_mas)
        self.div_botones_layout.addWidget(self.boton_menos)

        self.apuesta_layout.addWidget(self.label_apuesta_actual)
        self.apuesta_layout.addWidget(self.cant_apuesta_actual)
        self.apuesta_layout.addLayout(self.div_botones_layout)

        self.vbox.addStretch(1)

        self.vbox.addLayout(self.nombre_layout)
        self.vbox.addLayout(self.info_layout)
        self.vbox.addLayout(self.tragamonedas_layout)
        self.vbox.addLayout(self.apuesta_layout)


        self.show()

    def ingresar(self):

        self.line_edit.hide()
        self.label_nombre.hide()
        self.boton_entrar.hide()
        self.trigger_ingreso.emit(Ingreso(self.line_edit.text()))

    def aumentar(self):
        self.monto_apuesta += 500
        self.cant_apuesta_actual.setText("{}".format(self.monto_apuesta))

        if self.usuario_actual.saldo < self.monto_apuesta:
            self.boton_apostar.setEnabled(False)

    def disminuir(self):
        if not self.monto_apuesta - 500 < 0:
            self.monto_apuesta -= 500
        self.cant_apuesta_actual.setText("{}".format(self.monto_apuesta))

        if self.monto_apuesta <= self.usuario_actual.saldo:
            self.boton_apostar.setEnabled(True)


    def realizar_apuesta(self):
        self.trigger_apuesta.emit(Apostar(self.usuario_actual,
                                          self.monto_apuesta))

    def apostar1(self, evento):
        imagenes = evento.imagenes

        self.image1.setPixmap(QPixmap("imagenes/{}".format(imagenes[0]))
                              .scaled(100, 100))
        QTest.qWait(500)

        self.image2.setPixmap(QPixmap("imagenes/{}".format(imagenes[1]))
                              .scaled(100, 100))
        QTest.qWait(500)

        self.image3.setPixmap(QPixmap("imagenes/{}".format(imagenes[2]))
                              .scaled(100, 100))

        self.label_cant_saldo.setText("{}".format(evento.usuario.saldo))


if __name__ == '__main__':
    app = QApplication([])
    ventana = Ventana()
    app.exec_()
