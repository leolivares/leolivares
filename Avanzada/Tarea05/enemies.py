from PyQt5.QtCore import QThread, QTimer, QObject
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QTransform
from PyQt5 import uic, QtCore
from PyQt5.Qt import QTest
from PyQt5.QtWidgets import QLabel
from random import random, randint
from math import radians, cos, sin
import time

class Enemigo(QObject):

    id = 1
    pause = False

    def __init__(self, size):
        super().__init__()
        self.id = Enemigo.id
        self.size = size
        self._rotation = 0
        self.max_hp = (self.size * 20) + 100
        self._hp = self.max_hp
        self.damage = round((self.size * self.max_hp) / 10 , 0)
        self.img_act = "imagenes/e_walk1"
        self.ataque_actual = "imagenes/e_attack1"
        self.velocidad = 5
        self.gen_move = self.generador_move()
        self.gen_ataque = self.generador_ataque()
        self.stop_moving = False
        self.escape = False
        self.follow = False


        self.label = QLabel()
        pixmap = QPixmap("imagenes/e_walk1.png").scaled(self.size * 20, self.size * 20)
        diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        self.label.setMinimumSize(diag, diag)
        self.label.setMaximumSize(diag, diag)

        self.rango_vision = size * 30
        self.rango_escape = self.rango_vision * 1.3

        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.margen = diag // 2

        self._pos_x = randint(0, 730) + self.margen
        self._pos_y = randint(0, 590) + self.margen

        self.rotate = QTimer(self)
        self.rotate.setInterval(1000)
        self.rotate.timeout.connect(self.change_direction)
        self.rotate.start()

        self.walk = QTimer(self)
        self.walk.setInterval(150)
        self.walk.timeout.connect(self.move)
        self.walk.start()

        Enemigo.id += 1

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value >= 360:
            self._rotation = value - 360
        elif value < 0:
            self._rotation = 360 - abs(value)
        else:
            self._rotation = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value <= 0:
            self._hp = 0
        elif value > self.max_hp:
            self._hp = self.max_hp
        else:
            self._hp = value

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        if value > 730 + self.margen:
            self._pos_x = 730 + self.margen
        elif value < 0 + self.margen:
            self._pos_x = self.margen
        else:
            self._pos_x = value

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        if value > 590 + self.margen:
            self._pos_y = 590 + self.margen
        elif value < 0 + self.margen:
            self._pos_y = self.margen
        else:
            self._pos_y = value

    def generador_move(self):
        imgs = ["e_walk1", "e_walk2", "e_walk3", "e_walk4"]
        while True:
            for img in imgs:
                imagen_actual = "imagenes/" + img + ".png"
                yield imagen_actual

    def generador_ataque(self):
        imgs = ["e_attack2", "e_attack3", "e_attack4"]
        while True:
            for img in imgs:
                imagen_actual = "imagenes/" + img + ".png"
                yield imagen_actual

    def change_direction(self):
        if random() <= 0.25 and not self.stop_moving and not self.escape and not self.follow:
            self.rotation = randint(0, 360)

    def escape_player(self, angle, posx, posy):
        QTest.qWait(random()*1000)

        same_angle = angle
        changed_angle = angle + 180
        if changed_angle >= 360:
            changed_angle = changed_angle - 360

        x_same = self.pos_x + self.velocidad * cos(radians(same_angle))
        y_same = self.pos_y + self.velocidad * sin(radians(same_angle))
        x_changed = self.pos_x + self.velocidad * cos(radians(changed_angle))
        y_changed = self.pos_y + self.velocidad * sin(radians(changed_angle))


        diff_same = abs(posx - x_same) + abs(posy - y_same)
        diff_changed = abs(posx - x_changed) + abs(posy - y_changed)

        angulo_final = max([(same_angle, diff_same) ,
                            (changed_angle, diff_changed)],
                           key=lambda x: x[1])[0]

        self.rotation = angulo_final

    def follow_player(self, angle, posx, posy):
        QTest.qWait(random() * 1000)

        same_angle = angle
        changed_angle = angle + 180
        if changed_angle >= 360:
            changed_angle = changed_angle - 360

        x_same = self.pos_x + self.velocidad * cos(radians(same_angle))
        y_same = self.pos_y + self.velocidad * sin(radians(same_angle))
        x_changed = self.pos_x + self.velocidad * cos(radians(changed_angle))
        y_changed = self.pos_y + self.velocidad * sin(radians(changed_angle))

        diff_same = abs(posx - x_same) + abs(posy - y_same)
        diff_changed = abs(posx - x_changed) + abs(posy - y_changed)

        angulo_final = \
        min([(same_angle, diff_same), (changed_angle, diff_changed)],
            key=lambda x: x[1])[0]

        self.rotation = angulo_final

    def move(self):

        if not self.stop_moving and not Enemigo.pause and self.hp > 0:
            radianes = radians(self.rotation)

            x = self.velocidad * cos(radianes)
            y = self.velocidad * sin(radianes)

            if self.rotation >= 0 and self.rotation <= 90:
                x = abs(x)
                y = abs(y)
            elif self.rotation > 90 and self.rotation <= 180:
                x = abs(x) * -1
                y = abs(y)
            elif self.rotation > 180 and self.rotation <= 270:
                x = abs(x) * -1
                y = abs(y) * -1
            elif self.rotation > 270 and self.rotation <= 360:
                x = abs(x)
                y = abs(y) * -1

            x = round(x)
            y = round(y)

            self.pos_x += x
            self.pos_y += y

            self.img_act = next(self.gen_move)

    def attack(self, jugador):
        jugador.hp -= self.damage
        QTest.qWait(1000)