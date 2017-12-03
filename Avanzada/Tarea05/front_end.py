import sys
import time
from random import randint, choice
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QTransform, QIcon
from PyQt5.QtCore import QSize, Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QGraphicsView, QPushButton, QTableWidgetItem, QListWidgetItem, QHBoxLayout
from PyQt5.Qt import QTest, QSize, QSound
from players import Player
from enemies import Enemigo
from back_end import DCCell


formulario1 = uic.loadUiType("mainWindow.ui")
formulario2 = uic.loadUiType("one_player.ui")
formulario3 = uic.loadUiType("store.ui")
formulario4 = uic.loadUiType("highscores.ui")


class MainWindow(formulario1[0], formulario1[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.hswindow = HighScoreWindow()

        oImage = QImage("imagenes/posible_back.png")
        sImage = oImage.scaled(QSize(300, 200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.onePlayer.clicked.connect(self.one_player)
        self.hsBut.clicked.connect(self.mostrarHs)

    def one_player(self):
        nombre = self.lineEdit.text()
        self.one_p = GameWindow(nombre)
        self.one_p.show()
        self.close()

    def mostrarHs(self):
        self.hswindow.update_scores()
        self.hswindow.show()


class GameWindow(formulario2[0], formulario2[1]):

    trigger_start_game = pyqtSignal()
    trigger_stop_game = pyqtSignal()
    trigger_resume_game = pyqtSignal()
    trigger_exit_game = pyqtSignal(list)

    def __init__(self, name):
        super().__init__()
        self.setupUi(self)

        self.hswindow = HighScoreWindow()
        self.menu_principal = MainWindow()

        self.back = DCCell(self, 1)
        if len(name) != 0:
            self.name = name
            self.nombre_label.setText(name)
        else:
            self.name = "Player"
            self.nombre_label.setText("Player")

        oImage = QImage("imagenes/posible_back.png")
        sImage = oImage.scaled(QSize(300, 200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        oImage = QImage("imagenes/campo.png")
        sImage = oImage.scaled(QSize(300, 200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.gridFrame_2.setPalette(palette)

        self.store = StoreWindow(self.back.player1)

        pixmap_chest = QPixmap("imagenes/chest_cerrado.png").scaled(70, 70)

        self.inventario_layout = QHBoxLayout()
        self.item1_label = QLabel(self)
        self.item2_label = QLabel(self)
        self.item3_label = QLabel(self)
        self.item4_label = QLabel(self)
        self.item5_label = QLabel(self)

        self.inventario_labels = []
        self.inventario_labels.append(self.item1_label)
        self.inventario_labels.append(self.item2_label)
        self.inventario_labels.append(self.item3_label)
        self.inventario_labels.append(self.item4_label)
        self.inventario_labels.append(self.item5_label)

        self.item1_label.setFixedSize(pixmap_chest.size())
        self.item2_label.setFixedSize(pixmap_chest.size())
        self.item3_label.setFixedSize(pixmap_chest.size())
        self.item4_label.setFixedSize(pixmap_chest.size())
        self.item5_label.setFixedSize(pixmap_chest.size())

        self.inventario_layout.addWidget(self.item1_label)
        self.inventario_layout.addWidget(self.item2_label)
        self.inventario_layout.addWidget(self.item3_label)
        self.inventario_layout.addWidget(self.item4_label)
        self.inventario_layout.addWidget(self.item5_label)

        self.item1_label.setPixmap(pixmap_chest)
        self.item2_label.setPixmap(pixmap_chest)
        self.item3_label.setPixmap(pixmap_chest)
        self.item4_label.setPixmap(pixmap_chest)
        self.item5_label.setPixmap(pixmap_chest)

        self.verticalLayout.addLayout(self.inventario_layout)

        self.comienza = False
        self.pause = False

        self.storeBut.setEnabled(False)
        self.pauseBut.setEnabled(False)
        self.storeBut.clicked.connect(self.abrir_tienda)
        self.pauseBut.clicked.connect(self.pause_game)
        self.startBut.clicked.connect(self.start)
        self.exitBut.clicked.connect(self.exit)

        pixmap = QPixmap("imagenes/b_walk1.png").scaled(self.back.player1.size * 20, self.back.player1.size * 20)
        self.diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5

        self.player_label = QLabel(self)
        self.player_label.setMinimumSize(self.diag, self.diag)
        self.player_label.setMaximumSize(self.diag, self.diag)
        self.player_label.setAlignment(QtCore.Qt.AlignCenter)
        self.player_label.setPixmap(pixmap)
        self.player_label.move(350, 300)
        self.player_label.hide()

        self.player_label.setParent(self.gridFrame_2)

        self.enemy_labels = list()

        self.trigger_stop_game.connect(self.back.stop_game)
        self.trigger_resume_game.connect(self.back.resume_game)
        self.trigger_start_game.connect(self.back.start_game)
        self.trigger_exit_game.connect(self.back.new_highscore)

    def keyPressEvent(self, event):
        if not self.pause and self.comienza:
            if event.key() == Qt.Key_Escape:
                self.close()
            elif event.key() == Qt.Key_W:
                self.mover_adelante()
            elif event.key() == Qt.Key_S:
                self.mover_atras()
            elif event.key() == Qt.Key_A:
                self.levogiro()
            elif event.key() == Qt.Key_D:
                self.dextrogiro()

    def start(self):
        self.startBut.setEnabled(False)
        self.comienza = True
        self.player_label.show()
        self.trigger_start_game.emit()
        self.storeBut.setEnabled(True)
        self.pauseBut.setEnabled(True)

    def exit(self):
        self.trigger_stop_game.emit()
        self.trigger_exit_game.emit([self.name, self.back.player1.puntaje,
                                     self.back.nivel])
        self.hswindow.update_scores()
        self.hswindow.show()
        self.close()

    def abrir_tienda(self):
        QSound.play("audios/open_store.wav")
        self.store = StoreWindow(self.back.player1)
        self.store.setInventory()
        self.store.show()
        self.pause_game(True)

    def pause_game(self, audio=False):
        if not audio:
            QSound.play("audios/pause.wav")
        label = self.pauseBut.text()
        if label == "PAUSE":
            self.pause = True
            self.pauseBut.setText("RESUME")
            self.trigger_stop_game.emit()
            self.storeBut.setEnabled(False)

        elif label == "RESUME":
            self.pause = False
            self.pauseBut.setText("PAUSE")
            self.trigger_resume_game.emit()
            self.storeBut.setEnabled(True)
            self.store.close()
            self.actualizar_inventario()

    def actualizar_inventario(self):
        for item, label in zip(self.back.player1.items, self.inventario_labels):
            if item:
                label.setPixmap(QPixmap("imagenes/{0}.png".format(item)).scaled(70, 70))
            else:
                label.setPixmap(QPixmap("imagenes/chest_cerrado").scaled(70, 70))

    def actualizar_puntaje(self):
        self.puntaje_label.setText(str(self.back.player1.puntaje))

    def actualizar_exp(self):
        self.expBar.setValue(self.back.player1.exp)

    def aparicion_item(self, item):
        pixmap = QPixmap("imagenes/{}".format(item.item)).scaled(30, 35)
        diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5

        item.label.setMinimumSize(diag, diag)
        item.label.setMaximumSize(diag, diag)

        item.label.setPixmap(pixmap)
        item.label.setParent(self.gridFrame_2)
        item.label.move(item.pos_x - (item.label.width()//2), item.pos_y-(item.label.height()//2))
        item.label.show()

    def mover_adelante(self):

        pixmap = QPixmap("imagenes/b_walk1.png").scaled(
            self.back.player1.size * 20, self.back.player1.size * 20)
        self.diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        self.back.player1.margen = self.diag // 2
        self.back.player1.pos_x = self.player_label.x() + self.back.player1.margen
        self.back.player1.pos_y = self.player_label.y() + self.back.player1.margen

        player = self.back.player1
        mover_x, mover_y = player.mover_adelante()
        transform = QTransform().rotate(player.rotation)
        img = QPixmap(player.img_actual).scaled(player.size * 20, player.size * 20).transformed(transform,
                                                      QtCore.Qt.SmoothTransformation)

        self.player_label.setMinimumSize(self.diag, self.diag)
        self.player_label.setMaximumSize(self.diag, self.diag)


        self.player_label.setPixmap(QPixmap(img))
        self.player_label.move(mover_x-(self.player_label.width()//2), mover_y-(self.player_label.height()//2))

    def mover_atras(self):

        pixmap = QPixmap("imagenes/b_walk1.png").scaled(
            self.back.player1.size * 20, self.back.player1.size * 20)
        self.diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        self.back.player1.margen = self.diag // 2
        self.back.player1.pos_x = self.player_label.x() + self.back.player1.margen
        self.back.player1.pos_y = self.player_label.y() + self.back.player1.margen

        player = self.back.player1
        mover_x, mover_y = player.mover_atras()
        transform = QTransform().rotate(player.rotation)
        img = QPixmap(player.img_actual).scaled(player.size * 20, player.size * 20).transformed(transform,
                                                           QtCore.Qt.SmoothTransformation)

        self.player_label.setMinimumSize(self.diag, self.diag)
        self.player_label.setMaximumSize(self.diag, self.diag)

        self.player_label.setPixmap(QPixmap(img))
        self.player_label.move(mover_x-(self.player_label.width()//2), mover_y-(self.player_label.height()//2))

    def levogiro(self):
        pixmap = QPixmap("imagenes/b_walk1.png").scaled(
            self.back.player1.size * 20, self.back.player1.size * 20)
        self.diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        self.back.player1.margen = self.diag // 2
        self.back.player1.pos_x = self.player_label.x() + self.back.player1.margen
        self.back.player1.pos_y = self.player_label.y() + self.back.player1.margen

        player = self.back.player1

        player.girar_izq()
        transform = QTransform().rotate(player.rotation)
        img = QPixmap(player.img_actual).scaled(player.size * 20, player.size * 20).transformed(transform,
                                                 QtCore.Qt.SmoothTransformation)

        self.player_label.setMinimumSize(self.diag, self.diag)
        self.player_label.setMaximumSize(self.diag, self.diag)

        self.player_label.setPixmap(img)

    def dextrogiro(self):
        pixmap = QPixmap("imagenes/b_walk1.png").scaled(
            self.back.player1.size * 20, self.back.player1.size * 20)
        self.diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        self.back.player1.margen = self.diag // 2
        self.back.player1.pos_x = self.player_label.x() + self.back.player1.margen
        self.back.player1.pos_y = self.player_label.y() + self.back.player1.margen

        player = self.back.player1

        player.girar_der()
        transform = QTransform().rotate(player.rotation)
        img = QPixmap(player.img_actual).scaled(player.size * 20, player.size * 20).transformed(transform,
                                                           QtCore.Qt.SmoothTransformation)

        self.player_label.setMinimumSize(self.diag, self.diag)
        self.player_label.setMaximumSize(self.diag, self.diag)

        self.player_label.setPixmap(img)


    def nuevo_enemigo(self, enemigo):
        enemigo.label.setParent(self.gridFrame_2)
        self.enemy_labels.append((enemigo.label, enemigo.id))
        enemigo.label.move(enemigo.pos_x-enemigo.margen, enemigo.pos_y-enemigo.margen)
        enemigo.label.show()

    def move_enemy(self, enemigo):

        label = list(filter(lambda x: x[1] == enemigo.id,
                            self.enemy_labels))[0][0]

        transform = QTransform().rotate(enemigo.rotation)
        img = QPixmap(enemigo.img_act).scaled(enemigo.size * 20, enemigo.size * 20).transformed(transform,
                                                     QtCore.Qt.SmoothTransformation)

        label.move(enemigo.pos_x-(enemigo.label.width()//2), enemigo.pos_y-(enemigo.label.height()//2))
        label.setPixmap(img)

    def enemy_attack(self, enemigo):

        label = list(filter(lambda x: x[1] == enemigo.id,
                            self.enemy_labels))[0][0]
        for _ in range(4):
            QTest.qWait(25)
            transform = QTransform().rotate(enemigo.rotation)
            img = QPixmap(enemigo.ataque_actual).scaled(enemigo.size * 20, enemigo.size * 20).transformed(transform,
                                                       QtCore.Qt.SmoothTransformation)
            label.setPixmap(img)
            enemigo.ataque_actual = next(enemigo.gen_ataque)

        self.healthBar.setValue(self.back.player1.hp)

    def player_attack(self):

        player = self.back.player1
        for _ in range(4):
            QTest.qWait(25)
            transform = QTransform().rotate(self.back.player1.rotation)
            img = QPixmap(self.back.player1.att_actual).scaled(player.size * 20, player.size * 20).transformed(transform,
                                                         QtCore.Qt.SmoothTransformation)
            self.player_label.setPixmap(img)

            self.back.player1.att_actual = next(self.back.player1.gen_att)

    def esconder_jugador(self):
        if not self.back.player1.hidden:
            self.player_label.hide()

    def reaparecer(self):
        self.player_label.show()

    def actualizar_vida(self, item):
        item.label.hide()
        self.healthBar.setValue(self.back.player1.hp)

    def reajustar_puntaje(self, item):
        item.label.hide()
        self.puntaje_label.setText(str(self.back.player1.puntaje))

    def explosion(self, bomba):
        bomba.label.hide()

    def finalizar_juego(self):
        for label in self.enemy_labels:
            label[0].hide()
        over_label = QLabel()
        pixmap = QPixmap("imagenes/gameover.png").scaled(70, 70)
        over_label.setPixmap(pixmap)
        over_label.setParent(self.gridFrame_2)
        over_label.move(375, 300)
        over_label.show()
        QTest.qWait(10000)
        self.exit()

    def change_level(self, level):
        self.nivel_label.setText("NIVEL {}".format(str(level)))

    def maxhp(self, jugador):
        self.healthBar.setMaximum(jugador.max_hp)

class StoreWindow(formulario3[0], formulario3[1]):

    def __init__(self, jugador):
        super().__init__()
        self.setupUi(self)
        self.player = jugador

        oImage = QImage("imagenes/store_back.jpg")
        sImage = oImage.scaled(QSize(514, 290))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        icon_health = QIcon("imagenes/Vida.png")
        icon_strength = QIcon("imagenes/Fuerza.png")
        icon_quickness = QIcon("imagenes/Velocidad.png")

        entry1 = QListWidgetItem()
        entry2 = QListWidgetItem()
        entry3 = QListWidgetItem()

        entry1.setIcon(icon_health)
        entry2.setIcon(icon_quickness)
        entry3.setIcon(icon_strength)

        self.listWidget.addItem(entry1)
        self.listWidget.addItem(entry2)
        self.listWidget.addItem(entry3)

    def setInventory(self):

        for item in self.player.items:
            if not item:
                pixmap = QPixmap("imagenes/chest_cerrado.png").scaled(50, 50)
            else:
                pixmap = QPixmap("imagenes/{0}.png".format(item)).scaled(50, 50)

            item_label = NewQLabel(self.player)
            item_label.setFixedSize(pixmap.size())
            self.inventarioLayout.addWidget(item_label)
            item_label.setAcceptDrops(True)
            item_label.setPixmap(pixmap)


class NewQLabel(QLabel):

    id = 1

    def __init__(self, jugador, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = jugador
        self.id = NewQLabel.id
        NewQLabel.id += 1
        if NewQLabel.id == 6:
            NewQLabel.id = 1

    def dragEnterEvent(self, QDragEnterEvent):
        if QDragEnterEvent.source().currentRow() == 0:
            precio = 750
        elif QDragEnterEvent.source().currentRow() == 1:
            precio = 250
        else:
            precio = 500

        purchase = self.player.comprar(precio, self.id)

        if purchase:
            QDragEnterEvent.accept()

    def dropEvent(self, QDropEvent):

        if QDropEvent.source().currentRow() == 0:
            pixmap = QPixmap("imagenes/Vida.png").scaled(50, 50)
        elif QDropEvent.source().currentRow() == 1:
            pixmap = QPixmap("imagenes/Velocidad.png").scaled(50, 50)
        else:
            pixmap = QPixmap("imagenes/Fuerza.png").scaled(50, 50)

        self.setPixmap(pixmap)


class HighScoreWindow(formulario4[0], formulario4[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        oImage = QImage("imagenes/posible_back.png")
        sImage = oImage.scaled(QSize(300, 200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        items = (self.verticalLayout_2.itemAt(i) for i in range(self.verticalLayout_2.count()))
        i = 1
        for w in items:
            if w.widget():
                pixmap = QPixmap("imagenes/number{}".format(i)).scaled(15, 15)
                w.widget().setPixmap(pixmap)
                i += 1

    def update_scores(self):
        with open("highscores.txt", "r") as file:
            scores = [x.strip().split(",") for x in file]

        name_labels = [self.verticalLayout_3.itemAt(i)
                       for i in range(self.verticalLayout_3.count())
                       if isinstance(self.verticalLayout_3.itemAt(i).widget(),
                                     QLabel)][1:]
        score_labels = [self.verticalLayout_4.itemAt(i)
                        for i in range(self.verticalLayout_4.count())
                        if isinstance(self.verticalLayout_4.itemAt(i).widget(),
                                      QLabel)][1:]
        level_labels = [self.verticalLayout_5.itemAt(i)
                        for i in range(self.verticalLayout_5.count())
                        if isinstance(self.verticalLayout_5.itemAt(i).widget(),
                                      QLabel)][1:]

        for i in range(len(name_labels)):
            if isinstance(name_labels[i].widget(), QLabel) and name_labels[i].widget().text() != "Name":
                name_labels[i].widget().setText(scores[i][0])
                score_labels[i].widget().setText(scores[i][1])
                level_labels[i].widget().setText(scores[i][2])


if __name__ == '__main__':

    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())